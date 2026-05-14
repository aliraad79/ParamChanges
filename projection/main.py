from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from calculations.SimulationClass import SimulationClass
from calculations.config import default_config

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI()


def get_config(
    inflation_rate: float = default_config["INFLATION_RATE"],
    insurance_fee_from_salary: float = default_config["INSURANCE_FEE_FROM_SALARY"],
    simulation_years: int = default_config["SIMULATION_YEARS"],
    added_people_rate: float = default_config["EMPLOYED_AND_INSURED_RATE"],
    retirement_age: int = default_config["RETIREMENT_AGE"],
    basic_retirement_strategy: bool = default_config["BASIC_RETIREMENT_STRATEGY"],
    proposed_survivor_strategy: bool = default_config["PROPOSED_SURVIVOR_STRATEGY"],
    death_to_survivor_rate: float = default_config["DEATH_TO_SURVIVOR_RATE"],
    survivor_final_year_of_payroll: int = default_config["SURVIVOR_FINAL_YEAR_OF_PAYROLL"],
) -> dict:
    return {
        "INFLATION_RATE": inflation_rate,
        "INSURANCE_FEE_FROM_SALARY": insurance_fee_from_salary,
        "SIMULATION_YEARS": simulation_years,
        "EMPLOYED_AND_INSURED_RATE": added_people_rate,
        "RETIREMENT_AGE": retirement_age,
        "BASIC_RETIREMENT_STRATEGY": basic_retirement_strategy,
        "PROPOSED_SURVIVOR_STRATEGY": proposed_survivor_strategy,
        "DEATH_TO_SURVIVOR_RATE": death_to_survivor_rate,
        "SURVIVOR_FINAL_YEAR_OF_PAYROLL": survivor_final_year_of_payroll,
    }


@app.get("/api")
def json_report(config: dict = Depends(get_config)):
    sim = SimulationClass(config)
    sim.run()
    return sim.json_report()


@app.get("/api/human")
def human_report(config: dict = Depends(get_config)):
    sim = SimulationClass(config, cli=True)
    sim.run()
    return sim.human_json_report()


@app.get("/api/population")
def population_report(config: dict = Depends(get_config)):
    sim = SimulationClass(config)
    sim.run()
    return sim.population_json()


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
