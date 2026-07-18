"""Loads and provides access to the course/skill catalogue."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class Catalogue:
    """Wraps the course catalogue, skill dependency graph, and goal mappings."""

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            data_path = Path(__file__).resolve().parent.parent / "data" / "course_catalogue.json"
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.skills: Dict[str, dict] = data["skills"]
        self.courses: Dict[str, dict] = data["courses"]
        # Normalize goal keys to lowercase for forgiving matching.
        self.goals: Dict[str, List[str]] = {k.lower(): v for k, v in data["goals"].items()}

    def course_for_skill(self, skill: str) -> Optional[str]:
        skill_info = self.skills.get(skill)
        return skill_info["provided_by"] if skill_info else None

    def prerequisites_of(self, skill: str) -> List[str]:
        skill_info = self.skills.get(skill)
        return skill_info["prerequisites"] if skill_info else []

    def match_goal(self, goal_text: str) -> Optional[List[str]]:
        """Fuzzy-match a free-text goal string to a known goal's target skill list."""
        goal_text = goal_text.lower().strip()
        if goal_text in self.goals:
            return self.goals[goal_text]

        # Fall back to substring / keyword matching so phrasing like
        # "I want to become a Data Scientist" still resolves.
        best_match = None
        best_score = 0
        for goal_key, skill_list in self.goals.items():
            words = set(goal_key.split())
            overlap = sum(1 for w in words if w in goal_text)
            if overlap > best_score:
                best_score = overlap
                best_match = skill_list

        return best_match

    def course_info(self, course_id: str) -> dict:
        return self.courses[course_id]
