from fastapi import FastAPI
from calculations.SimulationClass import SimulationClass
from calculations.config import default_config


app = FastAPI()


@app.get("/")
def read_item(
    inflation_rate: float = default_config["INFLATION_RATE"],
    insurance_fee_from_salary: float = default_config["INSURANCE_FEE_FROM_SALARY"],
    simulation_years: int = default_config["SIMULATION_YEARS"],
    added_people_rate: float = default_config["ADDED_PEAOPLE_RATE"],
    retirment_age: int = default_config["RETIREMENTMENT_AGE"],
    basic_retirment_strategy: bool = default_config["BASIC_RETIRMENT_STRATEGY"],
    proposed_bazmandeh_strategy: bool = default_config["PROPOSED_BAZMANDEH_STRATEGY"],
    death_to_bazmandeh_rate: bool = default_config["DEATH_TO_BAZMANDEH_RATE"],
):
    config = {
        "INFLATION_RATE": inflation_rate,
        "INSURANCE_FEE_FROM_SALARY": insurance_fee_from_salary,
        "SIMULATION_YEARS": simulation_years,
        "ADDED_PEAOPLE_RATE": added_people_rate,
        "RETIREMENTMENT_AGE": retirment_age,
        "BASIC_RETIRMENT_STRATEGY": basic_retirment_strategy,
        "PROPOSED_BAZMANDEH_STRATEGY": proposed_bazmandeh_strategy,
        "DEATH_TO_BAZMANDEH_RATE": death_to_bazmandeh_rate,
    }
    mainClass = SimulationClass(config)
    mainClass.run()
    return mainClass.json_report()
