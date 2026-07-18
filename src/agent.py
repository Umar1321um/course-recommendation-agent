"""Core logic for the Course Recommendation Agent (Beginner)."""

from typing import List, Optional

from .catalogue import Catalogue
from .models import LearningPath, LearningStep, StudentProfile


class CourseRecommendationAgent:
    """
    Suggests a personalised, prerequisite-aware learning path for a student
    based on their background, goal, and current skills.
    """

    def __init__(self, catalogue: Optional[Catalogue] = None):
        self.catalogue = catalogue or Catalogue()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def recommend(self, profile: StudentProfile) -> LearningPath:
        target_skills = self.catalogue.match_goal(profile.goal)

        if not target_skills:
            return LearningPath(
                student_name=profile.name,
                goal=profile.goal,
                steps=[],
                already_known=profile.known_skills,
                unmet_goal_skills=[
                    f"Could not match goal '{profile.goal}' to a known career track."
                ],
            )

        known = set(profile.known_skills)
        ordered_skills = self._topological_skill_order(target_skills, known)

        steps: List[LearningStep] = []
        for i, skill in enumerate(ordered_skills, start=1):
            course_id = self.catalogue.course_for_skill(skill)
            if course_id is None:
                continue
            info = self.catalogue.course_info(course_id)
            reason = self._build_reason(skill, ordered_skills, target_skills)
            steps.append(
                LearningStep(
                    order=i,
                    course_id=course_id,
                    title=info["title"],
                    skill=skill,
                    level=info["level"],
                    reason=reason,
                )
            )

        already_known_target_skills = [s for s in target_skills if s in known]

        return LearningPath(
            student_name=profile.name,
            goal=profile.goal,
            steps=steps,
            already_known=already_known_target_skills,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _topological_skill_order(self, target_skills: List[str], known: set) -> List[str]:
        """
        Returns skills (not already known) in an order where every
        prerequisite skill appears before the skill that depends on it.
        """
        order: List[str] = []
        visited = set()

        def visit(skill: str):
            if skill in visited or skill in known:
                return
            visited.add(skill)
            for prereq in self.catalogue.prerequisites_of(skill):
                visit(prereq)
            if skill not in order:
                order.append(skill)

        for target in target_skills:
            visit(target)

        return order

    def _build_reason(self, skill: str, order: List[str], target_skills: List[str]) -> str:
        skill_name = skill.replace("_", " ")
        parts = []

        if skill in target_skills:
            parts.append(
                f"Teaches {skill_name}, one of the core skills required for your goal."
            )

        dependents = [
            s for s in order if skill in self.catalogue.prerequisites_of(s) and s != skill
        ]
        if dependents:
            dep_titles = []
            for dep in dependents:
                dep_course_id = self.catalogue.course_for_skill(dep)
                if dep_course_id:
                    dep_titles.append(self.catalogue.course_info(dep_course_id)["title"])
            if dep_titles:
                if len(dep_titles) == 1:
                    parts.append(
                        f"It is also a prerequisite for '{dep_titles[0]}' later in your path."
                    )
                else:
                    joined = ", ".join(f"'{t}'" for t in dep_titles)
                    parts.append(f"It is also a prerequisite for {joined}, later in your path.")

        if not parts:
            parts.append(
                f"Builds foundational knowledge ({skill_name}) needed to progress toward your goal."
            )

        return " ".join(parts)
