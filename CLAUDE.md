# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Analytical scripts and a simulation model for Iran's social-insurance system. Each top-level directory is an independent analysis answering a different policy question; they do not share code. There is no shared package and no linter configured — each sub-project is run on its own. Only the `projection/` sub-project has tests.

## Top-level layout

- `projection/` — FastAPI service that simulates the Social Security fund (sandogh) year-by-year over a configurable horizon. Inputs are demographic xlsx files in `projection/csv/`; outputs are JSON via HTTP. This is the only sub-project with a web/API surface and a Docker setup.
- `insurance_premium/` — One-shot script analyzing the 3% government share of insurance premium under different salary ceiling caps (`1x`, `2x`, `3x` of minimum wage). Writes CSV/PNG into `insurance_premium/csv/` and `insurance_premium/results/`.
- `unemployment/` — One-shot script computing unemployment-insurance cost figures for year 1396.
- `power-bi/` — Contains `Analytics-insurance.pbix` (Power BI binary report). Not code.

## Domain vocabulary (mixed Persian/English in code)

Identifiers freely mix Farsi transliteration with English. When editing or reading, recognize:

- `bazneshasteh` / `retired` — pensioners drawing retirement
- `azkaroftadeh` — disability pensioners (treated as constant in projection)
- `bazmandeh` / `survivor` — survivor beneficiaries (dependents of deceased)
- `bimeh pardaz` / `insured` — active premium-paying members
- `sandogh` — the insurance fund itself; `sandogh_income` vs. obligation drives solvency
- `hemat` — 10^12 rial (helper `rial_to_hemat` converts for display)
- `hage bimeh` — insurance premium
- Config keys live in `calculations/config.py` and are exposed verbatim as FastAPI query params via `main.py:get_config`. Renaming a key is a breaking API change for any existing caller.

## Running things

### projection (FastAPI simulation)

```bash
cd projection
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

xlsx inputs are resolved relative to the source tree (`Path(__file__).parent.parent / "csv"`), so the app also runs from any cwd.

Or via Docker:

```bash
cd projection
docker compose up        # API on :8080
```

Only `JSONReporter`, `HumanJSONReporter`, and `CLIReporter` are active in `report/reporter.py`.

Routes:

- `/` — static dashboard (HTML + Chart.js, in `projection/static/`). Persian/RTL, mirrors what the old `power-bi/Analytics-insurance.pbix` showed.
- `/api` — machine JSON report (per-year sandogh balance, populations, obligations)
- `/api/human` — formatted/human-readable JSON (also enables CLI printing)
- `/api/population` — `{year: {age_group: count}}` for the donut chart

All `/api/*` routes accept the same query params via the shared `get_config` dependency in `main.py` (defaults in `calculations/config.py`). The dashboard JS introspects `/openapi.json` at boot to populate default values in the form.

Runs on Python 3.12 (see `Dockerfile`), pandas 3.x, FastAPI 0.125+, Pydantic v2. Pins live in `requirements.txt` as compatible-range constraints, not exact versions — bump anything you like and rely on the snapshot test to catch behavioral drift.

### Tests

```bash
cd projection
pip install pytest
python -m pytest tests/
```

`tests/test_simulation.py` runs the simulation under default config and asserts the JSON output matches `tests/snapshot_default_config.json`. If you intentionally change simulation behavior, regenerate the snapshot:

```bash
python -c "import sys, json; sys.path.insert(0,'.'); \
  from calculations.SimulationClass import SimulationClass; \
  s=SimulationClass(); s.run(); \
  json.dump(s.json_report(), open('tests/snapshot_default_config.json','w'), indent=2, sort_keys=True)"
```

### insurance_premium

```bash
cd insurance_premium
pip install -r requirements.txt
python main.py        # writes CSVs to ./csv/, prints tables, generates plots
```

### unemployment

```bash
cd unemployment
python main.py        # writes ./csv/unimployment_direct.csv
```

## Architecture: projection simulation

This is the only piece with non-trivial structure. The pipeline lives in `projection/calculations/SimulationClass.py` and runs one tick per simulated year (`year` starts at 1400 Solar Hijri ≈ 2021 CE):

1. **Report** current state via `Reporter` (delegates to active reporters: JSON, HumanJSON, optionally CLI).
2. **Inflate** all salaries by `INFLATION_RATE` (`add_inflation_to_salaries`).
3. **Kill** — apply age-bucketed death rates (from `DEATH_BANDS` in `utils.py`) to retired, insured, and total population. Deaths from `insured` feed survivor inflow.
4. **Add survivors** from this year's deaths × `DEATH_TO_SURVIVOR_RATE`. If `PROPOSED_SURVIVOR_STRATEGY` is on, survivors are dropped after `SURVIVOR_FINAL_YEAR_OF_PAYROLL` years on payroll.
5. **Retire** members whose `insurance_record` ≥ `RETIREMENT_AGE` (`basic_bazneshastegi_rule`); `calculate_retirments` returns `(new_insured, new_retired)`.
6. **Add new insured** at age 30, sized from `population_projection.xlsx` × `EMPLOYED_AND_INSURED_RATE`.
7. **Age** every cohort (`age += 1`, `insurance_record += 1`).
8. If `BASIC_RETIREMENT_STRATEGY` is false, the retirement age ratchets up by 0.5/year (capped at 40) — this is the "advance retirement" policy lever.

Mortality lives in a single table — `DEATH_BANDS` in `calculations/utils.py` — as `(lower_inclusive, upper_exclusive, rate)` tuples. The original bands had off-by-one boundaries against the canonical 5-year groupings (e.g. the "15-19" rate covers ages 14-18) and gaps at ages 99 and 119 (death_percentage defaults to 0); these are preserved in the table to keep simulation output stable. Fix them deliberately and refresh the snapshot.

DataFrame helpers in `basic_utils.py` and `utils.py` return new DataFrames and do not mutate inputs — callers must reassign (`self.retired = add_to_ages(self.retired)`).

## Things to know before editing

- The three sub-projects do not share imports or utils. Adding helpers in one does not benefit the others.
- All xlsx/csv inputs in `projection/csv/` are real demographic data — do not delete or regenerate them.
- `main.py` exposes config via a single `Depends(get_config)` dependency; add new config keys there *and* in `calculations/config.py`.
- The `todo.md` in `projection/` is the active design log for the simulation; check it for context on partial features (e.g. "Add sandogh's sarmaye" — base capital — is still open).
- `static/` is plain HTML/CSS/JS — no build step. Chart.js is loaded from a CDN. If you add new chart fields, plumb them through `JSONReporter.add_report` in `report/JSONReporter.py` first, regenerate the snapshot, then read them in `static/app.js`.
