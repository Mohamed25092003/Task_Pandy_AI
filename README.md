# Task - Candidate Ranking CLI

This repository provides a small CLI to score and rank job candidates against job requirements using a weighted scoring model.

## Summary

The CLI reads job postings and candidate profiles from JSON files in `Data/`, preprocesses and normalizes them, applies a weighted scoring algorithm (weights defined in `WEIGHTS/Weights.py`), ranks candidates per job, and writes results to JSON files in `outputs/`.

This repository intentionally keeps dependencies minimal and uses only Python's standard library.

## Quick start

Prerequisites: Python 3.10+

Run the CLI via module mode or an interactive launcher:

Command-line examples:

```bash
# Rank candidates for a job (example)
python -m app rank --job-id j-001 --top-k 10 --out outputs/j-001.json

# Explain a single candidate vs job
python -m app explain --job-id j-001 --candidate-id c-001

# Run demo for all jobs and write to outputs/
python -m app demo --out-dir outputs/
```

Interactive mode:

```bash
# Start the interactive menu
python -m app
```
Then follow the prompts to run `rank`, `explain`, or `demo` without typing long flags.

Interactive sample session:

```
$ python -m app
Task interactive launcher
Commands:
	1) rank   - Rank candidates for a job
	2) explain - Explain candidate vs job
	3) demo   - Run demo for all jobs
	q) quit
Choose command: 1
Job id (e.g. j-001): j-001
Top k (leave empty for all): 5
Output path (e.g. outputs/j-001.json): outputs/j-001.json
```

## Interactive flow (menu)

```
app
├─ 1) rank     → asks for job id, top-k, output path
├─ 2) explain  → asks for job id, candidate id
└─ 3) demo     → asks for output directory
```

## Architecture (high level)

```
User (CLI / menu)
	│
	▼
cli/{rank,explain,demo}.py
	│
	▼
controllers/Preprocessing.py  → loads Data/*.json
	│
	▼
controllers/RankingController.py
	│
	▼
WEIGHTS/Weights.py  → weight coefficients
	│
	▼
outputs/*.json  (rank/demo) and console output (explain)
```

## Project structure

Root files and folders:

- `app/` — module wrapper to run CLI as `python -m app`
- `app/` — CLI and interactive menu launcher (`python -m app`)
- `cli/` — CLI command handlers (`rank.py`, `explain.py`, `demo.py`)
- `controllers/` — core logic (preprocessing, ranking controller)
- `WEIGHTS/` — scoring weights configuration
- `Data/` — input JSON files (`jobs.json`, `candidates.json`) and sample output
- `outputs/` — generated outputs (ignored by git)
- `pandy_ai/` — local virtualenv (should be ignored)
- `requirements.txt` — project requirements (standard library only)
- `.gitignore` — files/folders excluded from git

Key files:

- `cli/rank.py` — run ranking for a single job and write JSON
- `cli/explain.py` — print a detailed explanation for one candidate-job pair
- `cli/demo.py` — process all jobs and write aggregated output
- `controllers/Preprocessing.py` — reads and normalizes JSON input
- `controllers/RankingController.py` — scoring, ranking, and output formatting
- `WEIGHTS/Weights.py` — `Weights` Enum controlling scoring coefficients

Folder tree (simplified):

```
Task_Pandy_AI/
├── app/
├── cli/
│   ├── demo.py
│   ├── explain.py
│   └── rank.py
├── controllers/
│   ├── BaseController.py
│   ├── Preprocessing.py
│   └── RankingController.py
├── Data/
│   ├── candidates.json
│   ├── jobs.json
│   └── output.json
├── WEIGHTS/
│   └── Weights.py
├── outputs/
├── requirements.txt
└── .gitignore
```

## Data format

Input files live in `Data/`:

- `jobs.json` — list of job objects. Each job contains an `id`, `title`, `description`, and `requirements` (fields like `mustHaveSkills`, `niceToHaveSkills`, `minYears`, `location`).
- `candidates.json` — list of candidate objects. Each candidate contains `id`, `fullName`, `skills`, `yearsOfExperience`, `location`, `availability`, `score`, and other metadata.

Outputs are JSON files written to the `outputs/` directory by the `rank` and `demo` commands.

Sample data (from `Data/jobs.json`):

```json
{
	"id": "j-001",
	"title": "Frontend Engineer (React) — UI Craft",
	"description": "We’re building a design-forward recruitment platform...",
	"requirements": {
		"mustHaveSkills": ["React", "TypeScript", "CSS", "React Router"],
		"niceToHaveSkills": ["Accessibility", "Storybook", "Vitest"],
		"minYears": 3,
		"location": "Cairo, Egypt"
	}
}
```

Sample data (from `Data/candidates.json`):

```json
{
	"id": "c-001",
	"fullName": "Lina Hassan",
	"headline": "Frontend Engineer | React, TypeScript | Design Systems",
	"location": "Cairo, Egypt",
	"yearsOfExperience": 4,
	"skills": ["React", "TypeScript", "CSS", "Storybook", "Accessibility", "Jest"],
	"availability": "2 weeks",
	"score": 86
}
```

Sample output (rank result):

```json
{
	"j-001": [
		{
			"candidate_id": "c-001",
			"score": 0.8421,
			"matched_skills": ["react", "typescript", "css"],
			"missing_must_have_skills": ["react router"],
			"missing_nice_to_have_skills": ["vitest"],
			"summary": "Missing must-have skills: react router\nMissing nice-to-have skills: vitest\nCandidate meets or exceeds the experience requirement.\n"
		}
	]
}
```

## Scoring overview

Weights are defined in `WEIGHTS/Weights.py` and used by `RankingController` to compute a final score. Typical weights include:

- MUST_HAVE (e.g. 0.5)
- EXPERIENCE (e.g. 0.2)
- NICE_TO_HAVE (e.g. 0.15)
- LOCATION (e.g. 0.1)
- AVAILABILITY / FEEDBACK small bonuses/penalties

The controller extracts features per candidate-job pair (matched skills, missing skills, experience check, location match, availability, feedback) and computes a weighted score.

## Usage examples

- Rank top 10 candidates for `j-001` and save to `outputs/j-001.json`:

```bash
python -m app rank --job-id j-001 --top-k 10 --out outputs/j-001.json
```

Sample output (rank):

```json
[
	{
		"job_id": "j-001",
		"topk": 1,
		"results": {
			"candidate_id": "c-019",
			"score": 0.8476,
			"matched_skills": ["react", "react router", "typescript", "css"],
			"missing_must_have_skills": [],
			"missing_nice_to_have_skills": ["accessibility", "vitest", "storybook", "react query", "design tokens"],
			"summary": "All must-have skills matched which is ['react', 'react router', 'typescript', 'css']\nMissing nice-to-have skills: accessibility, vitest, storybook, react query, design tokens\nCandidate meets or exceeds the experience requirement.\n"
		},
		"meta": {
			"approach": "baseline-v1",
			"generatedAt": "2026-05-05T23:10:28.418616Z"
		}
	}
]
```

- Explain how candidate `c-001` scored for `j-001`:

```bash
python -m app explain --job-id j-001 --candidate-id c-001
```

Sample output (explain):

```
Explanation: c-001 vs j-001
Output: [{'job_id': 'j-001', 'results': {'candidate_id': 'c-001', 'score': 0.4623, 'matched_skills': ['react', 'storybook', 'accessibility', 'css', 'typescript'], 'missing_must_have_skills': ['react router'], 'missing_nice_to_have_skills': ['react query', 'design tokens', 'vitest'], 'summary': 'Missing must-have skills: react router\nMissing nice-to-have skills: react query, design tokens, vitest\nCandidate meets or exceeds the experience requirement.\n'}, 'meta': {'approach': 'baseline-v1', 'generatedAt': '2026-05-05T23:10:35.462322Z'}}]
```

- Run demo for all jobs and write aggregated output:

```bash
python -m app demo --out-dir outputs/
```

Sample output (demo):

```json
[
	{
		"job_id": "j-001",
		"topk": 1,
		"results": {
			"candidate_id": "c-019",
			"score": 0.8476,
			"matched_skills": ["css", "react", "typescript", "react router"],
			"missing_must_have_skills": [],
			"missing_nice_to_have_skills": ["accessibility", "vitest", "react query", "design tokens", "storybook"],
			"summary": "All must-have skills matched which is ['css', 'react', 'typescript', 'react router']\nMissing nice-to-have skills: accessibility, vitest, react query, design tokens, storybook\nCandidate meets or exceeds the experience requirement.\n"
		},
		"meta": {
			"approach": "baseline-v1",
			"generatedAt": "2026-05-05T23:10:40.484529Z"
		}
	}
]
```

- Interactive usage:

```bash
python -m app
```

## Notes & recommendations

- If you want reproducible environments, create `requirements.txt` (already present) and use a dedicated venv outside the repo, or add a small `pyproject.toml`/`venv` instructions.

## License

MIT
