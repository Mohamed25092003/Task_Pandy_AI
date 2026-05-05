# Task - Candidate Ranking CLI

This repository provides a small CLI called `task` to score and rank job candidates against job requirements using a weighted scoring model.

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
python -m task
```
Then follow the prompts to run `rank`, `explain`, or `demo` without typing long flags.

## Interactive flow (menu)

```
task
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
- `task/` — interactive menu launcher (`python -m task`)
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

## Data format

Input files live in `Data/`:

- `jobs.json` — list of job objects. Each job contains an `id`, `title`, `description`, and `requirements` (fields like `mustHaveSkills`, `niceToHaveSkills`, `minYears`, `location`).
- `candidates.json` — list of candidate objects. Each candidate contains `id`, `fullName`, `skills`, `yearsOfExperience`, `location`, `availability`, `score`, and other metadata.

Outputs are JSON files written to the `outputs/` directory by the `rank` and `demo` commands.

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

- Explain how candidate `c-001` scored for `j-001`:

```bash
python -m app explain --job-id j-001 --candidate-id c-001
```

- Run demo for all jobs and write aggregated output:

```bash
python -m app demo --out-dir outputs/
```

- Interactive usage:

```bash
python -m task
```

## Notes & recommendations

- The `pandy_ai/` virtual environment should be ignored in git (it is listed in `.gitignore`). If it was committed, remove it from tracking with:

```bash
git rm -r --cached pandy_ai/
git commit -m "Remove virtual environment from repo"
git push
```

- If you want reproducible environments, create `requirements.txt` (already present) and use a dedicated venv outside the repo, or add a small `pyproject.toml`/`venv` instructions.

## Contributing

Feel free to open issues or PRs to improve scoring, add tests, or extend the CLI.

## License

MIT
