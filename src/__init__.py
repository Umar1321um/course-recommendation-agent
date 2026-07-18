"""Course Recommendation Agent (Beginner) package."""

from .agent import CourseRecommendationAgent
from .catalogue import Catalogue
from .models import LearningPath, LearningStep, StudentProfile

__all__ = [
    "CourseRecommendationAgent",
    "Catalogue",
    "LearningPath",
    "LearningStep",
    "StudentProfile",
]
