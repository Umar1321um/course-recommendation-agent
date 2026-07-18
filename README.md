# Course Recommendation Agent (Beginner)

An AI agent that suggests a **personalised learning path** for a student based on their **background**, **career goal**, and **current skills** — by modeling a course catalogue with prerequisites and explaining *why* each course was chosen.

Live demo: _add your Render or ngrok link here once deployed_

---

## Table of Contents

- [What it does](#what-it-does)
- [Expected capabilities](#expected-capabilities)
- [How it works](#how-it-works)
- [Project structure](#project-structure)
- [Setup](#setup)
- [Ways to run it](#ways-to-run-it)
  - [1. Command line (sample profiles)](#1-command-line-sample-profiles)
  - [2. Command line (interactive)](#2-command-line-interactive)
  - [3. Web UI (browser)](#3-web-ui-browser)
- [Deploying it online](#deploying-it-online)
- [Running tests](#running-tests)
- [Sample profiles included](#sample-profiles-included)
- [Extending the catalogue](#extending-the-catalogue)
- [Run it on your own machine (localhost)](#run-it-on-your-own-machine-localhost)

---

## What it does

Give the agent a student's profile — their background, their goal (e.g. *"Data Scientist"*), and the skills they already know — and it returns a **step-by-step, prerequisite-ordered course plan**, with a plain-English reason for every single course it recommends.

## Expected capabilities

- Takes a student profile (background, goals, known skills) as input
- Models a small catalogue of courses/skills with prerequisites
- Recommends an ordered learning path with reasons for each step
- Explains why each course was chosen

## How it works

1. **Catalogue** (`data/course_catalogue.json`) defines:
   - `skills` — a dependency graph where each skill lists its prerequisite skills and the course that teaches it
   - `courses` — metadata (title, level, description) for each course
   - `goals` — maps a career goal (e.g. `"data scientist"`) to the target skills that goal requires
2. **Agent** (`src/agent.py`):
   - Resolves the student's goal to a target skill set (with fuzzy keyword matching for free-text goals)
   - Walks the prerequisite graph to find every skill the student needs but doesn't already have
   - Topologically sorts those skills so prerequisites always come before the courses that depend on them
   - Generates a human-readable rationale for every course: whether it directly teaches a goal skill, unlocks a later course, or both

No LLM is called at runtime — this is a deterministic, explainable graph algorithm, which means it's fast, free to run, and never hallucinates a course that doesn't exist.

## Project structure

```
course-recommendation-agent/
├── app.py                      # Flask web UI entry point
├── Procfile                    # Tells hosting services how to start the app
├── requirements.txt
├── README.md
├── LICENSE
├── data/
│   ├── course_catalogue.json   # Skills, courses, and goal mappings
│   └── sample_profiles.json    # 4 sample student profiles
├── docs/
│   └── sample_outputs.md       # Pre-generated recommended paths
├── src/
│   ├── models.py                # StudentProfile / LearningStep / LearningPath
│   ├── catalogue.py              # Loads and queries the catalogue
│   ├── agent.py                  # Core recommendation logic
│   └── main.py                   # CLI entry point (sample + interactive modes)
├── templates/
│   ├── index.html               # Web UI: profile form
│   └── result.html              # Web UI: recommended path display
├── static/
│   └── style.css                # Web UI styling
└── tests/
    └── test_agent.py            # Unit tests
```

## Setup

This project uses **pure Python standard library** for its core logic — no dependencies required to use the CLI. The web UI needs Flask.

```bash
git clone https://github.com/your-username/course-recommendation-agent.git
cd course-recommendation-agent
pip install -r requirements.txt
```

## Ways to run it

### 1. Command line (sample profiles)

Runs the agent against the 4 bundled sample profiles and prints each recommended path:

```bash
python -m src.main
```

Other flags:

```bash
python -m src.main --json                      # raw JSON output
python -m src.main --save-md docs/output.md    # save a Markdown report
python -m src.main --profiles-file path.json   # use your own profiles file
```

### 2. Command line (interactive)

Answers your questions directly in the terminal instead of editing a JSON file:

```bash
python -m src.main --interactive
```

You'll be asked for your name, background, goal, and known skills, and the agent prints (and can save) your personalised path.

### 3. Web UI (browser)

A form-based interface over the same agent logic, styled as an "enrollment ledger."

```bash
python app.py
```

Then open the link shown in the terminal — see [Run it on your own machine](#run-it-on-your-own-machine-localhost) below for full details.

## Deploying it online

Want a link you can share with anyone (recruiters, friends, an interviewer) without them needing Python installed?

**Free permanent hosting (recommended):**
1. Push your repo to GitHub (already done if you followed along)
2. Go to [render.com](https://render.com) → sign up free → **New +** → **Web Service**
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy — you'll get a permanent public URL like `https://course-recommendation-agent.onrender.com`

**Quick temporary link (share what's running right now):**
1. Install [ngrok](https://ngrok.com/download), sign up free, add your authtoken
2. Run `python app.py` in one terminal
3. Run `ngrok http 5000` in a second terminal
4. Share the `https://....ngrok-free.app` link it gives you (only works while both terminals stay open)

## Running tests

```bash
python tests/test_agent.py
```

or with pytest:

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

Full generated output for all four is in [`docs/sample_outputs.md`](docs/sample_outputs.md).

Supported goals out of the box: `web developer`, `frontend developer`, `backend developer`, `full stack developer`, `data analyst`, `data scientist`, `machine learning engineer`, `ai engineer`, `cloud engineer`, `devops engineer`.

## Extending the catalogue

Add a new skill/course by editing `data/course_catalogue.json`:

1. Add an entry under `"skills"` with its `prerequisites` and the `provided_by` course ID
2. Add the matching entry under `"courses"` with `title`, `skill`, `level`, and `description`
3. Optionally reference the new skill in one or more `"goals"` lists

No code changes are required — the agent reads the catalogue at runtime.

---

## Run it on your own machine (localhost)

Want to try it yourself, right now, on your own computer? Here's the complete path from zero to running:

**1. Make sure Python is installed**

```bash
python --version
```

Should show Python 3.8 or higher. If not, install it from [python.org](https://www.python.org/downloads/) (check "Add python.exe to PATH" during install).

**2. Get the code**

```bash
git clone https://github.com/your-username/course-recommendation-agent.git
cd course-recommendation-agent
```

**3. Install the one dependency needed for the web UI**

```bash
pip install -r requirements.txt
```

**4. Start the local server**

```bash
python app.py
```

You'll see:

```
* Running on http://127.0.0.1:5000
```

**5. Open it in your browser**

Go to **http://127.0.0.1:5000** in Chrome, Edge, or Firefox — on the **same computer** that's running the server (localhost only works locally unless you deploy it or tunnel it, see [Deploying it online](#deploying-it-online) above).

**6. Use it**

Fill in your name, background, career goal, and any skills you already know, then click **"Build my learning path →"** to see your personalised, prerequisite-ordered course plan.

**7. Stop the server**

Press `Ctrl+C` in the terminal when you're done.

Prefer the terminal over a browser? Skip the web UI entirely and run `python -m src.main --interactive` instead — same agent, plain-text answers.
