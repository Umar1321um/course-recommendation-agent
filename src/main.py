"""
CLI entry point for the Course Recommendation Agent (Beginner).

Usage:
    python -m src.main                       # run all sample profiles
    python -m src.main --interactive          # answer questions in the terminal
    python -m src.main --profiles-file path  # run profiles from a custom JSON file
    python -m src.main --json                # print raw JSON instead of formatted text
    python -m src.main --save-md path.md     # also save a Markdown report to disk
"""

import argparse
import json
from pathlib import Path
from typing import List

from src.agent import CourseRecommendationAgent
from src.models import LearningPath, StudentProfile


def load_profiles(path: str) -> List[StudentProfile]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [StudentProfile(**item) for item in raw]


def format_path_text(path: LearningPath) -> str:
    lines = []
    lines.append(f"Student: {path.student_name}")
    lines.append(f"Goal: {path.goal}")

    if path.already_known:
        known_str = ", ".join(s.replace("_", " ") for s in path.already_known)
        lines.append(f"Already has these goal-relevant skills: {known_str}")

    if path.unmet_goal_skills:
        for msg in path.unmet_goal_skills:
            lines.append(f"NOTE: {msg}")

    if not path.steps:
        lines.append("No further courses needed - all goal skills are already known!")
    else:
        lines.append("Recommended learning path:")
        for step in path.steps:
            lines.append(
                f"  {step.order}. [{step.course_id}] {step.title} ({step.level})"
            )
            lines.append(f"     Why: {step.reason}")

    return "\n".join(lines)


def format_path_markdown(path: LearningPath) -> str:
    lines = [f"## {path.student_name} â€” Goal: {path.goal}\n"]

    if path.already_known:
        known_str = ", ".join(s.replace("_", " ") for s in path.already_known)
        lines.append(f"**Already known goal-relevant skills:** {known_str}\n")

    if path.unmet_goal_skills:
        for msg in path.unmet_goal_skills:
            lines.append(f"> **Note:** {msg}\n")

    if not path.steps:
        lines.append("_No further courses needed - all goal skills are already known!_\n")
    else:
        lines.append("| # | Course ID | Title | Level | Reason |")
        lines.append("|---|-----------|-------|-------|--------|")
        for step in path.steps:
            lines.append(
                f"| {step.order} | {step.course_id} | {step.title} | {step.level} | {step.reason} |"
            )
        lines.append("")

    return "\n".join(lines)


def run_interactive():
    """Ask the student for their profile directly in the terminal."""
    from src.catalogue import Catalogue

    catalogue = Catalogue()
    agent = CourseRecommendationAgent(catalogue)

    print("=" * 60)
    print("Course Recommendation Agent - Interactive Mode")
    print("=" * 60)

    print("\nAvailable goals:")
    for goal_key in sorted(catalogue.goals.keys()):
        print(f"  - {goal_key.title()}")

    name = input("\nYour name: ").strip() or "Student"
    background = input("A little about your background: ").strip()
    goal = input("Your career goal (pick one from the list above): ").strip()

    skills_input = input(
        "Skills you already know, comma-separated (or press Enter for none)\n"
        "  e.g. python, html_css, statistics\n> "
    ).strip()
    known_skills = [s.strip() for s in skills_input.split(",") if s.strip()] if skills_input else []

    profile = StudentProfile(
        name=name,
        background=background,
        goal=goal,
        known_skills=known_skills,
    )

    path = agent.recommend(profile)

    print("\n" + "=" * 60)
    print(format_path_text(path))
    print("=" * 60)

    save = input("\nSave this as a Markdown file? (y/N): ").strip().lower()
    if save == "y":
        filename = input("Filename (default: my_learning_path.md): ").strip() or "my_learning_path.md"
        content = f"# Course Recommendation Agent â€” {profile.name}'s Learning Path\n\n"
        content += format_path_markdown(path)
        Path(filename).write_text(content, encoding="utf-8")
        print(f"Saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Course Recommendation Agent (Beginner)")
    parser.add_argument(
        "--profiles-file",
        default=str(Path(__file__).resolve().parent.parent / "data" / "sample_profiles.json"),
        help="Path to a JSON file with student profiles.",
    )
    parser.add_argument("--json", action="store_true", help="Print raw JSON output.")
    parser.add_argument("--save-md", help="Also save a Markdown report to this path.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Answer questions directly in the terminal instead of using a profiles file.",
    )
    args = parser.parse_args()

    if args.interactive:
        run_interactive()
        return

    profiles = load_profiles(args.profiles_file)
    agent = CourseRecommendationAgent()

    results = [agent.recommend(p) for p in profiles]

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        for r in results:
            print(format_path_text(r))
            print("-" * 60)

    if args.save_md:
        md_parts = ["# Course Recommendation Agent â€” Sample Outputs\n"]
        for r in results:
            md_parts.append(format_path_markdown(r))
        Path(args.save_md).write_text("\n".join(md_parts), encoding="utf-8")
        print(f"\nMarkdown report saved to {args.save_md}")


if __name__ == "__main__":
    main()