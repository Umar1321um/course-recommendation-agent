"""Data models used by the Course Recommendation Agent."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class StudentProfile:
    """Represents a student's background, goal, and current skills."""

    name: str
    background: str
    goal: str
    known_skills: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Normalize skill names to lowercase/underscored form for matching.
        self.known_skills = [s.strip().lower().replace(" ", "_") for s in self.known_skills]
        self.goal = self.goal.strip()


@dataclass
class LearningStep:
    """A single step (course) in a recommended learning path."""

    order: int
    course_id: str
    title: str
    skill: str
    level: str
    reason: str


@dataclass
class LearningPath:
    """The full ordered learning path recommended for a student."""

    student_name: str
    goal: str
    steps: List[LearningStep]
    already_known: List[str]
    unmet_goal_skills: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "student_name": self.student_name,
            "goal": self.goal,
            "already_known_skills": self.already_known,
            "recommended_path": [
                {
                    "order": s.order,
                    "course_id": s.course_id,
                    "title": s.title,
                    "skill": s.skill,
                    "level": s.level,
                    "reason": s.reason,
                }
                for s in self.steps
            ],
            "unmet_goal_skills": self.unmet_goal_skills,
        }
