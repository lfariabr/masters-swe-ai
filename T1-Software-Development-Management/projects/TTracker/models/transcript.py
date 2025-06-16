from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class Grade(str, Enum):
    """Standard grading scale."""
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D_PLUS = "D+"
    D = "D"
    F = "F"
    W = "W"  # Withdrawn
    I = "I"   # Incomplete
    P = "P"   # Pass
    NP = "NP" # No Pass

@dataclass
class CourseAttempt:
    """Represents a single attempt at a course."""
    code: str
    name: str
    semester: str  # e.g., "Fall 2023"
    credits_attempted: float
    credits_earned: float
    grade: Grade
    status: str  # e.g., "Completed", "In Progress", "Withdrawn"
    is_transfer: bool = False
    transfer_institution: Optional[str] = None

@dataclass
class Semester:
    """Represents an academic semester with its courses."""
    name: str  # e.g., "Fall 2023"
    start_date: datetime
    end_date: datetime
    gpa: Optional[float] = None
    credits_attempted: float = 0.0
    credits_earned: float = 0.0
    courses: List[CourseAttempt] = field(default_factory=list)

@dataclass
class Student:
    """Represents a student's academic information."""
    student_id: str
    full_name: str
    program: str
    program_code: str
    admission_date: datetime
    expected_graduation: Optional[datetime] = None
    current_gpa: Optional[float] = None
    cumulative_credits_attempted: float = 0.0
    cumulative_credits_earned: float = 0.0
    semesters: List[Semester] = field(default_factory=list)
    
    def get_course_history(self, course_code: str) -> List[CourseAttempt]:
        """Get all attempts for a specific course."""
        attempts = []
        for semester in self.semesters:
            for course in semester.courses:
                if course.code.lower() == course_code.lower():
                    attempts.append(course)
        return attempts

@dataclass
class AcademicRecord:
    """Complete academic record including all semesters and courses."""
    student: Student
    institution: str
    last_updated: datetime
    
    def to_dict(self) -> Dict:
        """Convert academic record to dictionary for serialization."""
        return {
            "student": {
                "student_id": self.student.student_id,
                "full_name": self.student.full_name,
                "program": self.student.program,
                "program_code": self.student.program_code,
                "admission_date": self.student.admission_date.isoformat(),
                "current_gpa": self.student.current_gpa,
                "cumulative_credits_attempted": self.student.cumulative_credits_attempted,
                "cumulative_credits_earned": self.student.cumulative_credits_earned
            },
            "institution": self.institution,
            "last_updated": self.last_updated.isoformat(),
            "semesters": [
                {
                    "name": sem.name,
                    "start_date": sem.start_date.isoformat(),
                    "end_date": sem.end_date.isoformat(),
                    "gpa": sem.gpa,
                    "credits_attempted": sem.credits_attempted,
                    "credits_earned": sem.credits_earned,
                    "courses": [
                        {
                            "code": c.code,
                            "name": c.name,
                            "semester": c.semester,
                            "credits_attempted": c.credits_attempted,
                            "credits_earned": c.credits_earned,
                            "grade": c.grade.value,
                            "status": c.status,
                            "is_transfer": c.is_transfer,
                            "transfer_institution": c.transfer_institution
                        } for c in sem.courses
                    ]
                } for sem in self.student.semesters
            ]
        }
