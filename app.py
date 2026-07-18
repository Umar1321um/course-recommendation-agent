"""
Flask web UI for the Course Recommendation Agent (Beginner).

Run locally with:
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template, request

from src.agent import CourseRecommendationAgent
from src.catalogue import Catalogue
from src.models import StudentProfile

app = Flask(__name__)

catalogue = Catalogue()
agent = CourseRecommendationAgent(catalogue)


def human_skill(skill_id: str) -> str:
    return skill_id.replace("_", " ").title()


@app.route("/", methods=["GET"])
def index():
    goals = sorted(catalogue.goals.keys())
    skills = sorted(catalogue.skills.keys())
    return render_template(
        "index.html",
        goals=goals,
        skills=skills,
        human_skill=human_skill,
    )


@app.route("/recommend", methods=["POST"])
def recommend():
    name = request.form.get("name", "").strip() or "Student"
    background = request.form.get("background", "").strip()
    goal = request.form.get("goal", "").strip()
    known_skills = request.form.getlist("known_skills")

    profile = StudentProfile(
        name=name,
        background=background,
        goal=goal,
        known_skills=known_skills,
    )

    path = agent.recommend(profile)

    return render_template(
        "result.html",
        path=path,
        human_skill=human_skill,
    )


if __name__ == "__main__":
    app.run(debug=True)
