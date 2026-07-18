"""
CLI entry point for the Course Recommendation Agent (Beginner).

Usage:
    python -m src.main                       # run all sample profiles
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
    lines = [f"## {path.student_name} — Goal: {path.goal}\n"]

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


def main():
    parser = argparse.ArgumentParser(description="Course Recommendation Agent (Beginner)")
    parser.add_argument(
        "--profiles-file",
        default=str(Path(__file__).resolve().parent.parent / "data" / "sample_profiles.json"),
        help="Path to a JSON file with student profiles.",
    )
    parser.add_argument("--json", action="store_true", help="Print raw JSON output.")
    parser.add_argument("--save-md", help="Also save a Markdown report to this path.")
    args = parser.parse_args()

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
        md_parts = ["# Course Recommendation Agent — Sample Outputs\n"]
        for r in results:
            md_parts.append(format_path_markdown(r))
        Path(args.save_md).write_text("\n".join(md_parts), encoding="utf-8")
        print(f"\nMarkdown report saved to {args.save_md}")


if __name__ == "__main__":
    main()
