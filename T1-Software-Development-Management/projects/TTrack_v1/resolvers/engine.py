# logic match transcript with the curriculum

import pandas as pd

def normalize_subject_codes(df, col='Subject Code'):
    """Standardize subject codes for accurate matching."""
    df[col] = df[col].astype(str).str.upper().str.strip()
    return df

def match_transcript_with_curriculum(transcript_df, curriculum_df):
    """
    Compare transcript and curriculum to classify subjects into:
    ✅ Done / ❌ Missing
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

def suggest_electives(result_df, max_electives=2):
    """
    Recommend missing electives from the curriculum.
    """
    missing_electives = result_df[
        (result_df['Type'].str.lower() == 'elective') &
        (result_df['Status'] == '❌ Missing')
    ]
    return missing_electives.head(max_electives)