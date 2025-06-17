from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Subject:
    """Represents a subject in the curriculum."""
    code: str
    name: str
    credits: float
    semester: int
    is_core: bool = True
    prerequisites: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class Program:
    """Represents an academic program with its curriculum."""
    name: str
    code: str
    total_credits: float
    required_credits: float
    elective_credits: float
    duration_years: int
    subjects: List[Subject] = field(default_factory=list)
    
    def get_subject_by_code(self, code: str) -> Optional[Subject]:
        """Get a subject by its code."""
        return next((s for s in self.subjects if s.code.lower() == code.lower()), None)
    
    def get_subjects_by_semester(self, semester: int) -> List[Subject]:
        """Get all subjects for a given semester."""
        return [s for s in self.subjects if s.semester == semester]

@dataclass
class Curriculum:
    """Represents the complete curriculum data structure."""
    program: Program
    version: str
    effective_date: datetime
    
    def to_dict(self) -> Dict:
        """Convert curriculum to dictionary for serialization."""
        return {
            "program": {
                "name": self.program.name,
                "code": self.program.code,
                "total_credits": self.program.total_credits,
                "required_credits": self.program.required_credits,
                "elective_credits": self.program.elective_credits,
                "duration_years": self.duration_years,
                "subjects": [
                    {
                        "code": s.code,
                        "name": s.name,
                        "credits": s.credits,
                        "semester": s.semester,
                        "is_core": s.is_core,
                        "prerequisites": s.prerequisites,
                        "description": s.description
                    } for s in self.program.subjects
                ]
            },
            "version": self.version,
            "effective_date": self.effective_date.isoformat()
        }
