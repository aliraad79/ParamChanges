from fastapi import FastAPI
from calculations.SimulationClass import SimulationClass
from calculations.config import default_config


app = FastAPI()


@app.get("/")
def read_item(
    inflation_rate: float = default_config["INFLATION_RATE"],
    insurance_fee_from_salary: float = default_config["INSURANCE_FEE_FROM_SALARY"],
    simulation_years: int = default_config["SIMULATION_YEARS"],
    added_people_rate: float = default_config["EMPLOYED_AND_INSURED_RATE"],
    retirement_age: int = default_config["RETIREMENTMENT_AGE"],
    basic_retirment_strategy: bool = default_config["BASIC_RETIRMENT_STRATEGY"],
    proposed_survivor_strategy: bool = default_config["PROPOSED_SURVIVOR_STRATEGY"],
    death_to_survivor_rate: bool = default_config["DEATH_TO_SURVIVOR_RATE"],
    survivor_final_yaer_of_payrool: int = default_config[
        "SURVIVOR_FINAL_YEAR_OF_PAYROOL"
    ],
):
    config = {
        "INFLATION_RATE": inflation_rate,
        "INSURANCE_FEE_FROM_SALARY": insurance_fee_from_salary,
        "SIMULATION_YEARS": simulation_years,
        "EMPLOYED_AND_INSURED_RATE": added_people_rate,
        "RETIREMENTMENT_AGE": retirement_age,
        "BASIC_RETIRMENT_STRATEGY": basic_retirment_strategy,
        "PROPOSED_SURVIVOR_STRATEGY": proposed_survivor_strategy,
        "DEATH_TO_SURVIVOR_RATE": death_to_survivor_rate,
        "SURVIVOR_FINAL_YEAR_OF_PAYROOL": survivor_final_yaer_of_payrool,
    }
    mainClass = SimulationClass(config)
    mainClass.run()
    return mainClass.json_report()


@app.get("/human")
def read_item(
    inflation_rate: float = default_config["INFLATION_RATE"],
    insurance_fee_from_salary: float = default_config["INSURANCE_FEE_FROM_SALARY"],
    simulation_years: int = default_config["SIMULATION_YEARS"],
    added_people_rate: float = default_config["EMPLOYED_AND_INSURED_RATE"],
    retirement_age: int = default_config["RETIREMENTMENT_AGE"],
    basic_retirment_strategy: bool = default_config["BASIC_RETIRMENT_STRATEGY"],
    proposed_survivor_strategy: bool = default_config["PROPOSED_SURVIVOR_STRATEGY"],
    death_to_survivor_rate: bool = default_config["DEATH_TO_SURVIVOR_RATE"],
    survivor_final_yaer_of_payrool: int = default_config[
        "SURVIVOR_FINAL_YEAR_OF_PAYROOL"
    ],
):
    config = {
        "INFLATION_RATE": inflation_rate,
        "INSURANCE_FEE_FROM_SALARY": insurance_fee_from_salary,
        "SIMULATION_YEARS": simulation_years,
        "EMPLOYED_AND_INSURED_RATE": added_people_rate,
        "RETIREMENTMENT_AGE": retirement_age,
        "BASIC_RETIRMENT_STRATEGY": basic_retirment_strategy,
        "PROPOSED_SURVIVOR_STRATEGY": proposed_survivor_strategy,
        "DEATH_TO_SURVIVOR_RATE": death_to_survivor_rate,
        "SURVIVOR_FINAL_YEAR_OF_PAYROOL": survivor_final_yaer_of_payrool,
    }
    mainClass = SimulationClass(config, cli=True)
    mainClass.run()
    return mainClass.human_json_report()


@app.get("/population")
def read_item(
    inflation_rate: float = default_config["INFLATION_RATE"],
    insurance_fee_from_salary: float = default_config["INSURANCE_FEE_FROM_SALARY"],
    simulation_years: int = default_config["SIMULATION_YEARS"],
    added_people_rate: float = default_config["EMPLOYED_AND_INSURED_RATE"],
    retirement_age: int = default_config["RETIREMENTMENT_AGE"],
    basic_retirment_strategy: bool = default_config["BASIC_RETIRMENT_STRATEGY"],
    proposed_survivor_strategy: bool = default_config["PROPOSED_SURVIVOR_STRATEGY"],
    death_to_survivor_rate: bool = default_config["DEATH_TO_SURVIVOR_RATE"],
    survivor_final_yaer_of_payrool: int = default_config[
        "SURVIVOR_FINAL_YEAR_OF_PAYROOL"
    ],
):
    config = {
        "INFLATION_RATE": inflation_rate,
        "INSURANCE_FEE_FROM_SALARY": insurance_fee_from_salary,
        "SIMULATION_YEARS": simulation_years,
        "EMPLOYED_AND_INSURED_RATE": added_people_rate,
        "RETIREMENTMENT_AGE": retirement_age,
        "BASIC_RETIRMENT_STRATEGY": basic_retirment_strategy,
        "PROPOSED_SURVIVOR_STRATEGY": proposed_survivor_strategy,
        "DEATH_TO_SURVIVOR_RATE": death_to_survivor_rate,
        "SURVIVOR_FINAL_YEAR_OF_PAYROOL": survivor_final_yaer_of_payrool,
    }
    mainClass = SimulationClass(config)
    mainClass.run()
    return mainClass.population_json()
