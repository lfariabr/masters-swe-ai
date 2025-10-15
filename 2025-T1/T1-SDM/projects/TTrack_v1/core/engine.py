# logic match transcript with the curriculum

import pandas as pd
from typing import List, Dict

# Global toggle: set to False to disable prerequisite checks across the engine
PREREQ_CHECK_ENABLED = False

def normalize_subject_codes(df, col='Subject Code'):
    """Standardize subject codes for accurate matching."""
    df = df.copy()
    df[col] = df[col].astype(str).str.upper().str.strip().str.replace(r'[^A-Z0-9]', '', regex=True)
    return df

def match_transcript_with_curriculum(transcript_df, curriculum_df):
    """
    Compare transcript and curriculum to classify subjects into:
    Done / Missing
    """
    # Normalize codes
    transcript_df = normalize_subject_codes(transcript_df)
    curriculum_df = normalize_subject_codes(curriculum_df)

    # Perform the match
    merged = curriculum_df.merge(
        transcript_df[['Subject Code']],
        on='Subject Code',
        how='left',
        indicator=True
    )

    merged['Status'] = merged['_merge'].map({
        'both': '✅ Done',
        'left_only': '❌ Missing'
    })

    # Select output columns
    result_df = merged[['Subject Code', 'Subject Name', 'Type', 'Status']]
    return result_df

def generate_progress_summary(result_df):
    """
    Returns a summary count by Type and Status.
    """
    # summary = result_df.groupby(['Type', 'Status']).size().unstack(fill_value=0)
    # return summary

    if result_df is None or result_df.empty:
        return None
        
    # Ensure we have the required columns
    if 'Type' not in result_df.columns or 'Status' not in result_df.columns:
        return None
    
    # Create the summary
    summary = result_df.groupby(['Type', 'Status']).size().unstack(fill_value=0)
    
    # Ensure we have consistent columns
    for status in ['✅ Done', '❌ Missing']:
        if status not in summary.columns:
            summary[status] = 0
    
    # Reset index to make Type a column
    summary = summary.reset_index()
    
    # Calculate total
    if not summary.empty:
        summary['Total'] = summary[['✅ Done', '❌ Missing']].sum(axis=1)
    
    return summary

def suggest_electives(result_df, max_electives=20):
    """
    Recommend missing electives from the curriculum.
    """
    missing_electives = result_df[
        (result_df['Type'].str.lower() == 'elective') &
        (result_df['Status'] == '❌ Missing')
    ]
    return missing_electives.head(max_electives)

def suggest_electives_v2(result_df: pd.DataFrame,
                         elective_bank_df: pd.DataFrame,
                         transcript_df: pd.DataFrame,
                         max_electives: int = 20) -> pd.DataFrame:
    transcript_codes = set(normalize_subject_codes(transcript_df)['Subject Code'])
    
    bank = normalize_subject_codes(elective_bank_df)

    # Filter out those already completed
    bank = bank[~bank['Subject Code'].isin(transcript_codes)].copy()

    if PREREQ_CHECK_ENABLED:
        def has_prereqs(row) -> bool:
            reqs = parse_prereqs(row.get('Prerequisites', ''))
            return all(req in transcript_codes for req in reqs)
        # Filter out those that don't meet prereqs
        bank['Eligible'] = bank.apply(has_prereqs, axis=1)
        recs = bank[bank['Eligible']].head(max_electives)
    else:
        # Show all not-yet-completed electives regardless of prerequisites
        recs = bank.head(max_electives)

    return recs[['Subject Code', 'Subject Name', 'Credit Points', 'Prerequisites']]

def parse_prereqs(prereq_str: str) -> List[str]:
    if not prereq_str:
        return []
    # split by commas/plus/space; keep only codes-ish tokens
    parts = [p.strip().upper() for p in re.split(r'[+,/]|\\band\\b|\\s+', prereq_str) if p.strip()]
    return [p for p in parts if re.match(r'^[A-Z]{2,}[0-9]{3}$', p)]

import re

def match_transcript_with_curriculum_v2(transcript_df: pd.DataFrame,
                                        curriculum_df: pd.DataFrame,
                                        elective_bank_df: pd.DataFrame) -> pd.DataFrame:
    # Normalize
    transcript_df = normalize_subject_codes(transcript_df, 'Subject Code')
    curriculum_df = normalize_subject_codes(curriculum_df, 'Subject Code')
    elective_bank_df = normalize_subject_codes(elective_bank_df, 'Subject Code')

    transcript_codes = set(transcript_df['Subject Code'].dropna().unique())
    elective_bank_codes = set(elective_bank_df['Subject Code'].dropna().unique())

    # --- Core matching by code
    cores = curriculum_df[curriculum_df['Type'].str.lower() == 'core'].copy()
    cores['Status'] = cores['Subject Code'].apply(lambda c: '✅ Done' if c in transcript_codes else '❌ Missing')
    cores['Filled By'] = ''

    # --- Elective slots filling
    # How many electives already completed? (intersection with bank)
    completed_electives = sorted(list(transcript_codes.intersection(elective_bank_codes)))
    n_completed = len(completed_electives)
    slots = curriculum_df[curriculum_df['Type'].str.lower() == 'elective'].copy().reset_index(drop=True)

    def slot_row(i: int) -> Dict:
        row = slots.iloc[i].to_dict()
        row_code = row['Subject Code']
        if i < n_completed:
            # mark slot "Done" and annotate which elective satisfied it
            row['Status'] = '✅ Done'
            row['Filled By'] = completed_electives[i]  # which elective code satisfied this slot
        else:
            row['Status'] = '❌ Missing'
            row['Filled By'] = ''
        return row

    filled_slots = pd.DataFrame([slot_row(i) for i in range(len(slots))])

    # --- Optional: prerequisite check (boolean flag)
    def prereq_met(row) -> bool:
        reqs = parse_prereqs(row.get('Prerequisites', ''))
        if not reqs:
            return True
        return all(req in transcript_codes for req in reqs)

    if PREREQ_CHECK_ENABLED:
        cores['PrereqMet'] = cores.apply(prereq_met, axis=1)
    else:
        cores['PrereqMet'] = True  # prereq checks disabled
    filled_slots['PrereqMet'] = True  # elective slots don’t have prereqs; actual chosen electives are validated by bank entries

    # Final result
    result_df = pd.concat([cores, filled_slots], ignore_index=True)

    # Making a better ordering
    cols = ['Subject Code', 'Subject Name', 'Type', 'Credit Points', 'Prerequisites', 'Status']
    if 'Filled By' in result_df.columns:
        cols.append('Filled By')
    cols.append('PrereqMet')
    return result_df[cols]

def generate_progress_summary_v2(result_df: pd.DataFrame) -> pd.DataFrame:
    if result_df is None or result_df.empty:
        return None
    
    summary = result_df.groupby(['Type', 'Status']).size().unstack(fill_value=0).reset_index()
    for status in ['✅ Done', '❌ Missing']:
        if status not in summary.columns:
            summary[status] = 0
    
    summary['Total'] = summary[['✅ Done', '❌ Missing']].sum(axis=1)
    
    # Completion % by type
    summary['Completion %'] = (summary['✅ Done'] / summary['Total']).round(2)
    summary['Completion %'] = summary['Completion %'].apply(lambda x: f"{x*100}%")
    # Removing ".0" from Completion %
    summary['Completion %'] = summary['Completion %'].str.replace('.0%', '%')

    return summary