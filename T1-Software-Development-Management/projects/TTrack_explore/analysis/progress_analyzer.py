from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime

from models.curriculum import Curriculum, Subject
from models.transcript import AcademicRecord, CourseAttempt, Grade

class RequirementStatus(Enum):
    """Status of a curriculum requirement."""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class RequirementResult:
    """Result of evaluating a single requirement."""
    code: str
    name: str
    status: RequirementStatus
    credits_earned: float = 0.0
    credits_required: float = 0.0
    completion_ratio: float = 0.0
    details: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'code': self.code,
            'name': self.name,
            'status': self.status.name,
            'credits_earned': self.credits_earned,
            'credits_required': self.credits_required,
            'completion_ratio': self.completion_ratio,
            'details': self.details
        }

@dataclass
class ProgressResult:
    """Overall progress result for a student."""
    student_id: str
    student_name: str
    program: str
    program_code: str
    current_gpa: Optional[float] = None
    total_credits_attempted: float = 0.0
    total_credits_earned: float = 0.0
    completion_ratio: float = 0.0
    requirements: List[RequirementResult] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'student_id': self.student_id,
            'student_name': self.student_name,
            'program': self.program,
            'program_code': self.program_code,
            'current_gpa': self.current_gpa,
            'total_credits_attempted': self.total_credits_attempted,
            'total_credits_earned': self.total_credits_earned,
            'completion_ratio': self.completion_ratio,
            'requirements': [req.to_dict() for req in self.requirements]
        }

class ProgressAnalyzer:
    """Analyzes student progress against a curriculum."""
    
    def __init__(self, curriculum: Curriculum, academic_record: AcademicRecord):
        """Initialize with curriculum and academic record."""
        self.curriculum = curriculum
        self.academic_record = academic_record
        self.completed_courses: Dict[str, List[CourseAttempt]] = {}
        self.failed_courses: Dict[str, List[CourseAttempt]] = {}
        self._process_course_history()
    
    def _process_course_history(self) -> None:
        """Process the student's course history to categorize completed and failed courses."""
        self.completed_courses = {}
        self.failed_courses = {}
        
        for semester in self.academic_record.student.semesters:
            for course in semester.courses:
                course_code = course.code.upper()
                
                # Skip courses with no grade or in-progress courses
                if course.grade in [Grade.I, Grade.W]:
                    continue
                
                # Categorize as completed or failed
                if course.grade in [Grade.F, Grade.NP]:
                    if course_code not in self.failed_courses:
                        self.failed_courses[course_code] = []
                    self.failed_courses[course_code].append(course)
                else:
                    if course_code not in self.completed_courses:
                        self.completed_courses[course_code] = []
                    self.completed_courses[course_code].append(course)
    
    def analyze_progress(self) -> ProgressResult:
        """Analyze the student's progress against the curriculum."""
        student = self.academic_record.student
        program = self.curriculum.program
        
        # Initialize result
        result = ProgressResult(
            student_id=student.student_id,
            student_name=student.full_name,
            program=program.name,
            program_code=program.code,
            current_gpa=student.current_gpa,
            total_credits_attempted=student.cumulative_credits_attempted,
            total_credits_earned=student.cumulative_credits_earned,
            completion_ratio=(
                student.cumulative_credits_earned / program.total_credits
                if program.total_credits > 0 else 0.0
            )
        )
        
        # Analyze core requirements
        core_credits_earned = self._analyze_core_requirements(program, result)
        
        # Analyze elective requirements
        elective_credits_earned = self._analyze_elective_requirements(program, result)
        
        # Update completion ratio based on actual requirements
        total_required = program.required_credits + program.elective_credits
        if total_required > 0:
            result.completion_ratio = (
                (core_credits_earned + elective_credits_earned) / total_required
            )
        
        return result
    
    def _analyze_core_requirements(
        self,
        program: 'Program',
        result: ProgressResult
    ) -> float:
        """Analyze core requirements and return total core credits earned."""
        core_subjects = [s for s in program.subjects if s.is_core]
        core_credits_earned = 0.0
        
        # Track which core subjects have been completed
        for subject in core_subjects:
            subject_code = subject.code.upper()
            attempts = self.completed_courses.get(subject_code, [])
            
            if attempts:
                # Take the most recent attempt
                latest_attempt = max(attempts, key=lambda x: x.semester)
                core_credits_earned += latest_attempt.credits_earned
                status = RequirementStatus.COMPLETED
            elif subject_code in self.failed_courses:
                status = RequirementStatus.FAILED
            else:
                status = RequirementStatus.NOT_STARTED
            
            result.requirements.append(RequirementResult(
                code=subject.code,
                name=subject.name,
                status=status,
                credits_earned=sum(a.credits_earned for a in attempts),
                credits_required=subject.credits,
                completion_ratio=(
                    sum(a.credits_earned for a in attempts) / subject.credits
                    if subject.credits > 0 else 1.0
                ),
                details={
                    'is_core': True,
                    'semester': subject.semester,
                    'latest_attempt': (
                        max(attempts, key=lambda x: x.semester).grade.value
                        if attempts else None
                    )
                }
            ))
        
        return core_credits_earned
    
    def _analyze_elective_requirements(
        self,
        program: 'Program',
        result: ProgressResult
    ) -> float:
        """Analyze elective requirements and return total elective credits earned."""
        if program.elective_credits <= 0:
            return 0.0
        
        # Get all completed courses that aren't core requirements
        core_codes = {s.code.upper() for s in program.subjects if s.is_core}
        elective_attempts = []
        
        for course_code, attempts in self.completed_courses.items():
            if course_code not in core_codes:
                elective_attempts.extend(attempts)
        
        # Sort by semester to get most recent grades for each course
        elective_attempts.sort(key=lambda x: x.semester)
        
        # Deduplicate by course code, keeping the most recent attempt
        unique_electives = {}
        for attempt in elective_attempts:
            unique_electives[attempt.code.upper()] = attempt
        
        # Calculate total elective credits
        total_elective_credits = sum(a.credits_earned for a in unique_electives.values())
        
        # Add elective requirement result
        result.requirements.append(RequirementResult(
            code="ELECTIVE",
            name="Elective Courses",
            status=(
                RequirementStatus.COMPLETED
                if total_elective_credits >= program.elective_credits
                else RequirementStatus.IN_PROGRESS
            ),
            credits_earned=total_elective_credits,
            credits_required=program.elective_credits,
            completion_ratio=(
                min(total_elective_credits / program.elective_credits, 1.0)
                if program.elective_credits > 0 else 1.0
            ),
            details={
                'is_core': False,
                'courses_completed': [
                    {
                        'code': a.code,
                        'name': a.name,
                        'credits': a.credits_earned,
                        'grade': a.grade.value,
                        'semester': a.semester
                    } for a in unique_electives.values()
                ]
            }
        ))
        
        return min(total_elective_credits, program.elective_credits)
    
    def check_prerequisites(self, subject: Subject) -> Tuple[bool, List[str]]:
        """Check if prerequisites are met for a subject.
        
        Returns:
            Tuple of (all_prerequisites_met, [missing_prerequisites])
        """
        if not subject.prerequisites:
            return True, []
        
        missing = []
        for prereq in subject.prerequisites:
            prereq = prereq.upper()
            if prereq not in self.completed_courses:
                missing.append(prereq)
        
        return len(missing) == 0, missing
    
    def get_recommended_courses(self, semester: int) -> List[Subject]:
        """Get recommended courses for a given semester based on progress."""
        # Get subjects for the target semester
        target_subjects = [
            s for s in self.curriculum.program.subjects 
            if s.semester == semester
        ]
        
        recommended = []
        for subject in target_subjects:
            # Skip already completed courses
            if subject.code.upper() in self.completed_courses:
                continue
                
            # Check prerequisites
            prereqs_met, _ = self.check_prerequisites(subject)
            if prereqs_met:
                recommended.append(subject)
        
        return recommended
