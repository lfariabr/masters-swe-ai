"""
Tests for the curriculum matching engine.
"""
import pytest
import pandas as pd
from resolvers.engine import (
    match_transcript_with_curriculum,
    generate_progress_summary,
    suggest_electives,
    normalize_subject_codes
)

# Sample test data
SAMPLE_CURRICULUM = pd.DataFrame({
    'Subject Code': ['MATH101', 'PHYS101', 'ELEC101', 'ELEC102', 'CORE101'],
    'Subject Name': ['Calculus I', 'Physics I', 'Elective I', 'Elective II', 'Core Subject'],
    'Type': ['Core', 'Core', 'Elective', 'Elective', 'Core'],
    'Credits': [3, 4, 3, 3, 3]
})

SAMPLE_TRANSCRIPT = pd.DataFrame({
    'Subject Code': ['MATH101', 'PHYS101', 'ELEC101'],
    'Subject Name': ['Calculus I', 'Physics I', 'Elective I'],
    'Grade': ['A', 'B+', 'A-'],
    'Credits': [3, 4, 3]
})

class TestCurriculumMatching:
    """Test cases for the curriculum matching engine."""
    
    def test_normalize_subject_codes(self):
        """Test that subject codes are properly normalized."""
        test_df = pd.DataFrame({
            'Subject Code': [' math101 ', 'PHYS101', '  elec101  ']
        })
        
        result = normalize_subject_codes(test_df)
        
        expected = ['MATH101', 'PHYS101', 'ELEC101']
        assert list(result['Subject Code']) == expected
    
    def test_match_transcript_complete(self):
        """Test matching a complete transcript against the curriculum."""
        result = match_transcript_with_curriculum(SAMPLE_TRANSCRIPT, SAMPLE_CURRICULUM)
        
        # Check that all curriculum items are present in the result
        assert set(SAMPLE_CURRICULUM['Subject Code']).issubset(set(result['Subject Code']))
        
        # Check status of matched items
        status = result.set_index('Subject Code')['Status']
        assert status['MATH101'] == '✅ Done'
        assert status['PHYS101'] == '✅ Done'
        assert status['ELEC101'] == '✅ Done'
        assert status['ELEC102'] == '❌ Missing'
        assert status['CORE101'] == '❌ Missing'
    
    def test_generate_progress_summary(self):
        """Test generation of progress summary."""
        result = match_transcript_with_curriculum(SAMPLE_TRANSCRIPT, SAMPLE_CURRICULUM)
        summary = generate_progress_summary(result)
        
        # Check that summary contains expected columns
        expected_columns = {'Type', '✅ Done', '❌ Missing', 'Total'}
        assert set(summary.columns) == expected_columns
        
        # Check specific counts
        summary_dict = summary.set_index('Type')
        
        # Check Core subjects
        core_row = summary_dict.loc['Core']
        assert core_row['✅ Done'] == 2  # MATH101, PHYS101
        assert core_row['❌ Missing'] == 1  # CORE101
        assert core_row['Total'] == 3  # Total Core subjects
        
        # Check Elective subjects
        elec_row = summary_dict.loc['Elective']
        assert elec_row['✅ Done'] == 1  # ELEC101
        assert elec_row['❌ Missing'] == 1  # ELEC102
        assert elec_row['Total'] == 2  # Total Elective subjects
    
    def test_suggest_electives(self):
        """Test elective suggestion functionality."""
        result = match_transcript_with_curriculum(SAMPLE_TRANSCRIPT, SAMPLE_CURRICULUM)
        suggestions = suggest_electives(result, max_electives=1)
        
        # Should suggest the missing elective
        assert len(suggestions) == 1
        assert suggestions.iloc[0]['Subject Code'] == 'ELEC102'
    
    def test_empty_transcript(self):
        """Test with an empty transcript."""
        empty_transcript = pd.DataFrame(columns=['Subject Code', 'Subject Name', 'Grade', 'Credits'])
        result = match_transcript_with_curriculum(empty_transcript, SAMPLE_CURRICULUM)
        
        # All curriculum items should be missing
        status = result.set_index('Subject Code')['Status']
        assert all(status == '❌ Missing')

# Fixture for sample data
@pytest.fixture
def sample_curriculum():
    """Fixture providing sample curriculum data."""
    return SAMPLE_CURRICULUM.copy()

@pytest.fixture
def sample_transcript():
    """Fixture providing sample transcript data."""
    return SAMPLE_TRANSCRIPT.copy()
