import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

from models.transcript import AcademicRecord, Student, Semester, CourseAttempt, Grade

class TranscriptLoader:
    """
    Loads and parses student transcript data from Excel files.
    
    Expected Excel format:
    - First sheet contains student information
    - Subsequent sheets contain course attempts by semester
    """
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize the transcript loader with the path to the Excel file."""
        self.file_path = Path(file_path)
        self.xls = pd.ExcelFile(self.file_path)
    
    def load(self) -> AcademicRecord:
        """Load and parse the transcript data from the Excel file."""
        # Load student information from the first sheet
        student_info = self._load_student_info()
        
        # Create student
        student = Student(
            student_id=student_info['student_id'],
            full_name=student_info['full_name'],
            program=student_info['program'],
            program_code=student_info['program_code'],
            admission_date=student_info['admission_date'],
            expected_graduation=student_info.get('expected_graduation'),
            current_gpa=student_info.get('current_gpa'),
            cumulative_credits_attempted=student_info.get('cumulative_credits_attempted', 0.0),
            cumulative_credits_earned=student_info.get('cumulative_credits_earned', 0.0)
        )
        
        # Load semesters and course attempts
        semesters = []
        for sheet_name in self.xls.sheet_names[1:]:  # Skip the first sheet (student info)
            try:
                semester_info = self._load_semester(sheet_name)
                if semester_info:
                    semesters.append(semester_info)
            except Exception as e:
                print(f"Error loading semester {sheet_name}: {e}")
        
        # Sort semesters by start date
        semesters.sort(key=lambda x: x.start_date)
        student.semesters = semesters
        
        # Create and return academic record
        return AcademicRecord(
            student=student,
            institution=student_info.get('institution', 'Unknown'),
            last_updated=student_info.get('last_updated', datetime.now())
        )
    
    def _load_student_info(self) -> Dict:
        """Load student information from the first sheet."""
        df = pd.read_excel(self.file_path, sheet_name=0, header=None)
        info = {}
        
        # Convert to dictionary with first column as keys and second as values
        for _, row in df.iterrows():
            if len(row) >= 2 and pd.notna(row[0]) and pd.notna(row[1]):
                key = str(row[0]).strip().lower().replace(' ', '_')
                value = row[1]
                info[key] = value
        
        # Convert date fields
        date_fields = ['admission_date', 'expected_graduation', 'last_updated']
        for field in date_fields:
            if field in info and isinstance(info[field], str):
                try:
                    info[field] = datetime.strptime(info[field], '%Y-%m-%d')
                except (ValueError, TypeError):
                    if field != 'expected_graduation':  # This one is optional
                        info[field] = datetime.now()
        
        # Convert numeric fields
        numeric_fields = ['current_gpa', 'cumulative_credits_attempted', 'cumulative_credits_earned']
        for field in numeric_fields:
            if field in info:
                try:
                    info[field] = float(info[field])
                except (ValueError, TypeError):
                    info[field] = 0.0
        
        return info
    
    def _load_semester(self, sheet_name: str) -> Optional[Semester]:
        """Load semester data from a sheet."""
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            
            # Clean up column names
            df.columns = [str(col).strip().lower() for col in df.columns]
            
            # Extract semester info (assuming first row contains semester info)
            semester_name = str(sheet_name).strip()
            start_date = None
            end_date = None
            gpa = None
            
            # Try to extract dates and GPA from the first row if they exist
            if not df.empty:
                first_row = df.iloc[0]
                if 'start_date' in first_row and pd.notna(first_row['start_date']):
                    try:
                        start_date = pd.to_datetime(first_row['start_date']).to_pydatetime()
                    except:
                        pass
                if 'end_date' in first_row and pd.notna(first_row['end_date']):
                    try:
                        end_date = pd.to_datetime(first_row['end_date']).to_pydatetime()
                    except:
                        pass
                if 'gpa' in first_row and pd.notna(first_row['gpa']):
                    try:
                        gpa = float(first_row['gpa'])
                    except (ValueError, TypeError):
                        pass
            
            # Create semester
            semester = Semester(
                name=semester_name,
                start_date=start_date or datetime.now(),
                end_date=end_date or datetime.now(),
                gpa=gpa
            )
            
            # Process course attempts
            courses = []
            for _, row in df.iterrows():
                try:
                    # Skip rows that don't have course code or name
                    if pd.isna(row.get('code')) or pd.isna(row.get('name')):
                        continue
                    
                    # Parse grade
                    grade_str = str(row.get('grade', '')).strip().upper()
                    try:
                        grade = Grade(grade_str) if grade_str in Grade._value2member_map_ else Grade.P
                    except ValueError:
                        grade = Grade.P  # Default to Pass if grade is not recognized
                    
                    # Parse credits
                    credits_attempted = float(row.get('credits_attempted', row.get('credits', 0)))
                    credits_earned = float(row.get('credits_earned', credits_attempted if grade not in [Grade.F, Grade.NP, Grade.W] else 0))
                    
                    # Create course attempt
                    course = CourseAttempt(
                        code=str(row['code']).strip(),
                        name=str(row['name']).strip(),
                        semester=semester_name,
                        credits_attempted=credits_attempted,
                        credits_earned=credits_earned,
                        grade=grade,
                        status=row.get('status', 'Completed'),
                        is_transfer=bool(row.get('is_transfer', False)),
                        transfer_institution=str(row.get('transfer_institution', '')).strip() or None
                    )
                    courses.append(course)
                except Exception as e:
                    print(f"Error parsing course in row {_}: {e}")
            
            # Update semester with courses and credits
            semester.courses = courses
            semester.credits_attempted = sum(c.credits_attempted for c in courses)
            semester.credits_earned = sum(c.credits_earned for c in courses)
            
            return semester
            
        except Exception as e:
            print(f"Error loading semester {sheet_name}: {e}")
            return None

def load_transcript(file_path: Union[str, Path]) -> Optional[AcademicRecord]:
    """Convenience function to load transcript from a file."""
    try:
        loader = TranscriptLoader(file_path)
        return loader.load()
    except Exception as e:
        print(f"Error loading transcript: {e}")
        return None
