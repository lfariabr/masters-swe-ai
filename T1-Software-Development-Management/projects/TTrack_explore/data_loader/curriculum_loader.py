import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from models.curriculum import Curriculum, Program, Subject

class CurriculumLoader:
    """
    Loads and parses curriculum data from Excel files.
    
    Expected Excel format:
    - First sheet contains program information
    - Subsequent sheets contain subject lists by semester
    """
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize the curriculum loader with the path to the Excel file."""
        self.file_path = Path(file_path)
        self.xls = pd.ExcelFile(self.file_path)
    
    def load(self) -> Curriculum:
        """Load and parse the curriculum data from the Excel file."""
        # Load program information from the first sheet
        program_info = self._load_program_info()
        
        # Load subjects from all sheets (except the first one)
        subjects = []
        for sheet_name in self.xls.sheet_names[1:]:  # Skip the first sheet (program info)
            try:
                semester = int(sheet_name.split()[-1])  # Extract semester number from sheet name
                subjects.extend(self._load_subjects(sheet_name, semester))
            except (ValueError, IndexError):
                print(f"Warning: Could not determine semester from sheet name: {sheet_name}")
        
        # Create program with subjects
        program = Program(
            name=program_info['program_name'],
            code=program_info['program_code'],
            total_credits=program_info['total_credits'],
            required_credits=program_info['required_credits'],
            elective_credits=program_info['elective_credits'],
            duration_years=program_info['duration_years'],
            subjects=subjects
        )
        
        # Create and return curriculum
        return Curriculum(
            program=program,
            version=program_info.get('version', '1.0'),
            effective_date=program_info.get('effective_date', datetime.now())
        )
    
    def _load_program_info(self) -> Dict:
        """Load program information from the first sheet."""
        df = pd.read_excel(self.file_path, sheet_name=0, header=None)
        info = {}
        
        # Convert to dictionary with first column as keys and second as values
        for _, row in df.iterrows():
            if len(row) >= 2 and pd.notna(row[0]) and pd.notna(row[1]):
                key = str(row[0]).strip().lower().replace(' ', '_')
                value = row[1]
                info[key] = value
        
        # Convert numeric fields
        numeric_fields = ['total_credits', 'required_credits', 'elective_credits', 'duration_years']
        for field in numeric_fields:
            if field in info:
                try:
                    info[field] = float(info[field])
                except (ValueError, TypeError):
                    info[field] = 0.0
        
        # Convert date field
        if 'effective_date' in info and isinstance(info['effective_date'], str):
            try:
                info['effective_date'] = datetime.strptime(info['effective_date'], '%Y-%m-%d')
            except ValueError:
                info['effective_date'] = datetime.now()
        
        return info
    
    def _load_subjects(self, sheet_name: str, semester: int) -> List[Subject]:
        """Load subjects from a specific semester sheet."""
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            
            # Clean up column names (remove extra spaces, make lowercase)
            df.columns = [str(col).strip().lower() for col in df.columns]
            
            # Ensure required columns exist
            required_columns = ['code', 'name', 'credits']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Required column '{col}' not found in sheet: {sheet_name}")
            
            subjects = []
            for _, row in df.iterrows():
                try:
                    # Skip rows with missing required fields
                    if any(pd.isna(row[col]) for col in required_columns):
                        continue
                    
                    # Parse prerequisites if the column exists
                    prerequisites = []
                    if 'prerequisites' in df.columns and pd.notna(row.get('prerequisites')):
                        prereq_str = str(row['prerequisites']).strip()
                        if prereq_str:
                            # Split by comma or other common separators
                            prerequisites = [p.strip() for p in prereq_str.replace(';', ',').split(',') if p.strip()]
                    
                    # Create subject
                    subject = Subject(
                        code=str(row['code']).strip(),
                        name=str(row['name']).strip(),
                        credits=float(row['credits']),
                        semester=semester,
                        is_core=bool(row.get('is_core', True)),
                        prerequisites=prerequisites,
                        description=str(row.get('description', '')).strip()
                    )
                    subjects.append(subject)
                except Exception as e:
                    print(f"Error parsing subject in row {_}: {e}")
            
            return subjects
            
        except Exception as e:
            print(f"Error loading sheet {sheet_name}: {e}")
            return []

def load_curriculum(file_path: Union[str, Path]) -> Optional[Curriculum]:
    """Convenience function to load curriculum from a file."""
    try:
        loader = CurriculumLoader(file_path)
        return loader.load()
    except Exception as e:
        print(f"Error loading curriculum: {e}")
        return None
