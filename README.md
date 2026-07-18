# Course Recommendation Agent (Beginner)

Suggests a personalised learning path for a student based on their
**background**, **goal**, and **current skills** — modeling a small course
catalogue with prerequisites and explaining *why* each course was chosen.

## Expected Capabilities

- Takes a student profile (background, goals, known skills) as input
- Models a small catalogue of courses/skills with prerequisites
- Recommends an ordered learning path with reasons for each step
- Explains why each course was chosen

## How it works

1. **Catalogue** (`data/course_catalogue.json`) defines:
   - `skills`: a dependency graph where each skill lists its prerequisite
     skills and the course that teaches it.
   - `courses`: metadata (title, level, description) for each course.
   - `goals`: maps a career goal (e.g. `"data scientist"`) to the set of
     target skills that goal requires.
2. **Agent** (`src/agent.py`):
   - Resolves the student's goal to a target skill set (with fuzzy
     keyword matching for free-text goals).
   - Walks the prerequisite graph to find every skill the student needs
     but doesn't already have.
   - Topologically sorts those skills so prerequisites always come
     before the courses that depend on them.
   - Generates a human-readable rationale for every course: whether it
     directly teaches a goal skill, unlocks a later course, or both.

## Project structure

```
course-recommendation-agent/
├── data/
│   ├── course_catalogue.json   # Skills, courses, and goal mappings
│   └── sample_profiles.json    # 4 sample student profiles
├── docs/
│   └── sample_outputs.md       # Pre-generated recommended paths (deliverable)
├── src/
│   ├── models.py               # StudentProfile / LearningStep / LearningPath
│   ├── catalogue.py            # Loads and queries the catalogue
│   ├── agent.py                # Core recommendation logic
│   └── main.py                 # CLI entry point
├── tests/
│   └── test_agent.py           # Unit tests
├── requirements.txt
└── README.md
```

## Usage

Run against the bundled sample profiles:

```bash
python3 -m src.main
```

Print raw JSON instead:

```bash
python3 -m src.main --json
```

Save a Markdown report (used to generate `docs/sample_outputs.md`):

```bash
python3 -m src.main --save-md docs/sample_outputs.md
```

Use your own profiles file (same shape as `data/sample_profiles.json`):

```bash
python3 -m src.main --profiles-file path/to/your_profiles.json
```

### Profile format

```json
{
  "name": "Asha",
  "background": "Second-year commerce student with no coding experience.",
  "goal": "Data Analyst",
  "known_skills": []
}
```

Supported goals out of the box: `web developer`, `frontend developer`,
`backend developer`, `full stack developer`, `data analyst`,
`data scientist`, `machine learning engineer`, `ai engineer`,
`cloud engineer`, `devops engineer`. Free-text goals containing these
words (e.g. "I want to become a Data Scientist") are matched too.

## Running tests

```bash
python3 tests/test_agent.py
```

or, with pytest installed:

```bash
pytest tests/
```

## Sample profiles included

| Name   | Background                                             | Goal                     | Known skills                              |
|--------|----------------------------------------------------------|---------------------------|--------------------------------------------|
| Asha   | Commerce student, no coding experience                   | Data Analyst              | none                                        |
| Rahul  | Hobbyist who built static HTML/CSS pages                 | Full Stack Developer      | html_css                                    |
| Meera  | Mechanical engineering grad, strong math                 | Machine Learning Engineer | linear_algebra, statistics                  |
| Vikram | Junior backend developer, writes Python & basic APIs     | Cloud Engineer            | programming_basics, python, backend_dev     |

Full generated output for all four profiles is in
[`docs/sample_outputs.md`](docs/sample_outputs.md).

## Extending the catalogue

Add a new skill/course by editing `data/course_catalogue.json`:

1. Add an entry under `"skills"` with its `prerequisites` and the
   `provided_by` course ID.
2. Add the matching entry under `"courses"` with `title`, `skill`,
   `level`, and `description`.
3. Optionally reference the new skill in one or more `"goals"` lists.

No code changes are required — the agent reads the catalogue at runtime.
Course Recommendation Agent (Beginner)
Suggests a personalised learning path for a student based on their
background, goal, and current skills — modeling a small course
catalogue with prerequisites and explaining why each course was chosen.
Expected Capabilities
Takes a student profile (background, goals, known skills) as input
Models a small catalogue of courses/skills with prerequisites
Recommends an ordered learning path with reasons for each step
Explains why each course was chosen
How it works
Catalogue (`data/course_catalogue.json`) defines:
`skills`: a dependency graph where each skill lists its prerequisite
skills and the course that teaches it.
`courses`: metadata (title, level, description) for each course.
`goals`: maps a career goal (e.g. `"data scientist"`) to the set of
target skills that goal requires.
Agent (`src/agent.py`):
Resolves the student's goal to a target skill set (with fuzzy
keyword matching for free-text goals).
Walks the prerequisite graph to find every skill the student needs
but doesn't already have.
Topologically sorts those skills so prerequisites always come
before the courses that depend on them.
Generates a human-readable rationale for every course: whether it
directly teaches a goal skill, unlocks a later course, or both.
Project structure
```
course-recommendation-agent/
├── data/
│   ├── course_catalogue.json   # Skills, courses, and goal mappings
│   └── sample_profiles.json    # 4 sample student profiles
├── docs/
│   └── sample_outputs.md       # Pre-generated recommended paths (deliverable)
├── src/
│   ├── models.py               # StudentProfile / LearningStep / LearningPath
│   ├── catalogue.py            # Loads and queries the catalogue
│   ├── agent.py                # Core recommendation logic
│   └── main.py                 # CLI entry point
├── tests/
│   └── test_agent.py           # Unit tests
├── requirements.txt
└── README.md
```
Web UI (runs locally in your browser)
A small local web app (`app.py`, built with Flask) provides a form-based UI
over the same agent logic:
```bash
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 in your browser. Fill in your name,
background, goal, and any known skills, and it renders your personalised
learning path as a visual route with reasons for each stop.
Usage
Run against the bundled sample profiles:
```bash
python3 -m src.main
```
Interactive mode
Answer questions directly in the terminal instead of editing a JSON file:
```bash
python3 -m src.main --interactive
```
You'll be asked for your name, background, goal, and known skills, and the
agent will print (and optionally save) your personalised learning path.
Print raw JSON instead:
```bash
python3 -m src.main --json
```
Save a Markdown report (used to generate `docs/sample_outputs.md`):
```bash
python3 -m src.main --save-md docs/sample_outputs.md
```
Use your own profiles file (same shape as `data/sample_profiles.json`):
```bash
python3 -m src.main --profiles-file path/to/your_profiles.json
```
Profile format
```json
{
  "name": "Asha",
  "background": "Second-year commerce student with no coding experience.",
  "goal": "Data Analyst",
  "known_skills": []
}
```
Supported goals out of the box: `web developer`, `frontend developer`,
`backend developer`, `full stack developer`, `data analyst`,
`data scientist`, `machine learning engineer`, `ai engineer`,
`cloud engineer`, `devops engineer`. Free-text goals containing these
words (e.g. "I want to become a Data Scientist") are matched too.
Running tests
```bash
python3 tests/test_agent.py
```
or, with pytest installed:
```bash
pytest tests/
```
Sample profiles included
Name	Background	Goal	Known skills
Asha	Commerce student, no coding experience	Data Analyst	none
Rahul	Hobbyist who built static HTML/CSS pages	Full Stack Developer	html_css
Meera	Mechanical engineering grad, strong math	Machine Learning Engineer	linear_algebra, statistics
Vikram	Junior backend developer, writes Python & basic APIs	Cloud Engineer	programming_basics, python, backend_dev
Full generated output for all four profiles is in
`docs/sample_outputs.md`.
Extending the catalogue
Add a new skill/course by editing `data/course_catalogue.json`:
Add an entry under `"skills"` with its `prerequisites` and the
`provided_by` course ID.
Add the matching entry under `"courses"` with `title`, `skill`,
`level`, and `description`.
Optionally reference the new skill in one or more `"goals"` lists.
No code changes are required — the agent reads the catalogue at runtime.