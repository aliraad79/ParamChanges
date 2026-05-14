from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from calculations.SimulationClass import SimulationClass
from calculations.config import default_config

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI()


class SimulationConfig(BaseModel):
    inflation_rate: float = Field(default=default_config["INFLATION_RATE"])
    insurance_fee_from_salary: float = Field(default=default_config["INSURANCE_FEE_FROM_SALARY"])
    simulation_years: int = Field(default=default_config["SIMULATION_YEARS"])
    added_people_rate: float = Field(default=default_config["EMPLOYED_AND_INSURED_RATE"])
    retirement_age: int = Field(default=default_config["RETIREMENT_AGE"])
    basic_retirement_strategy: bool = Field(default=default_config["BASIC_RETIREMENT_STRATEGY"])
    proposed_survivor_strategy: bool = Field(default=default_config["PROPOSED_SURVIVOR_STRATEGY"])
    death_to_survivor_rate: float = Field(default=default_config["DEATH_TO_SURVIVOR_RATE"])
    survivor_final_year_of_payroll: int = Field(default=default_config["SURVIVOR_FINAL_YEAR_OF_PAYROLL"])

    def to_internal(self) -> dict:
        return {
            "INFLATION_RATE": self.inflation_rate,
            "INSURANCE_FEE_FROM_SALARY": self.insurance_fee_from_salary,
            "SIMULATION_YEARS": self.simulation_years,
            "EMPLOYED_AND_INSURED_RATE": self.added_people_rate,
            "RETIREMENT_AGE": self.retirement_age,
            "BASIC_RETIREMENT_STRATEGY": self.basic_retirement_strategy,
            "PROPOSED_SURVIVOR_STRATEGY": self.proposed_survivor_strategy,
            "DEATH_TO_SURVIVOR_RATE": self.death_to_survivor_rate,
            "SURVIVOR_FINAL_YEAR_OF_PAYROLL": self.survivor_final_year_of_payroll,
        }


@lru_cache(maxsize=64)
def _run_cached(config_key: tuple, cli: bool = False) -> SimulationClass:
    """Run sim for a frozen config; lets sibling endpoints share work."""
    config = dict(config_key)
    sim = SimulationClass(config, cli=cli)
    sim.run()
    return sim


def _run(body: SimulationConfig, cli: bool = False) -> SimulationClass:
    return _run_cached(tuple(sorted(body.to_internal().items())), cli=cli)


@app.post("/api")
def json_report(config: SimulationConfig):
    return _run(config).json_report()


@app.post("/api/human")
def human_report(config: SimulationConfig):
    return _run(config, cli=True).human_json_report()


@app.post("/api/population")
def population_report(config: SimulationConfig):
    return _run(config).population_json()


@app.post("/api/full")
def full_report(config: SimulationConfig):
    """Per-year report + per-year age-bracket populations in one round trip."""
    sim = _run(config)
    return {
        "report": sim.json_report(),
        "population": sim.population_json(),
    }


@app.get("/api/defaults")
def defaults() -> dict:
    """Exposed so the dashboard can pre-fill the config form."""
    return SimulationConfig().model_dump()


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
