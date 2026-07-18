"""Basic tests for the Course Recommendation Agent."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import CourseRecommendationAgent
from src.catalogue import Catalogue
from src.models import StudentProfile


def make_agent():
    return CourseRecommendationAgent(Catalogue())


def test_prerequisites_come_before_dependents():
    agent = make_agent()
    profile = StudentProfile(
        name="Test Student",
        background="No experience.",
        goal="Data Analyst",
        known_skills=[],
    )
    path = agent.recommend(profile)
    course_ids = [s.course_id for s in path.steps]

    # Python (CS102) must come before Data Analysis (DS101)
    assert course_ids.index("CS102") < course_ids.index("DS101")
    # Programming basics (CS101) must come before Python (CS102)
    assert course_ids.index("CS101") < course_ids.index("CS102")
    # Statistics (MATH101) must come before Data Analysis (DS101)
    assert course_ids.index("MATH101") < course_ids.index("DS101")


def test_known_skills_are_skipped():
    agent = make_agent()
    profile = StudentProfile(
        name="Test Student",
        background="Has basic web skills.",
        goal="Frontend Developer",
        known_skills=["html_css"],
    )
    path = agent.recommend(profile)
    course_ids = [s.course_id for s in path.steps]

    # WD101 (HTML & CSS) should be skipped since it's already known.
    assert "WD101" not in course_ids
    assert "html_css" in path.already_known


def test_every_step_has_a_reason():
    agent = make_agent()
    profile = StudentProfile(
        name="Test Student",
        background="Curious beginner.",
        goal="Cloud Engineer",
        known_skills=[],
    )
    path = agent.recommend(profile)
    assert len(path.steps) > 0
    for step in path.steps:
        assert step.reason and len(step.reason) > 0


def test_unmatched_goal_reports_note():
    agent = make_agent()
    profile = StudentProfile(
        name="Test Student",
        background="Undecided.",
        goal="Astronaut",
        known_skills=[],
    )
    path = agent.recommend(profile)
    assert path.steps == []
    assert len(path.unmet_goal_skills) == 1


def test_all_goal_skills_already_known_produces_empty_path():
    agent = make_agent()
    profile = StudentProfile(
        name="Test Student",
        background="Experienced cloud dev.",
        goal="Cloud Engineer",
        known_skills=["python", "cloud_fundamentals", "devops_basics"],
    )
    path = agent.recommend(profile)
    assert path.steps == []
    assert set(path.already_known) == {"python", "cloud_fundamentals", "devops_basics"}


if __name__ == "__main__":
    test_prerequisites_come_before_dependents()
    test_known_skills_are_skipped()
    test_every_step_has_a_reason()
    test_unmatched_goal_reports_note()
    test_all_goal_skills_already_known_produces_empty_path()
    print("All tests passed!")
