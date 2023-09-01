from fastapi import FastAPI
from calculations.SimulationClass import SimulationClass

app = FastAPI()


@app.get("/")
def read_item(
    inflation_rate: float = 0.46,
    insurance_fee_from_salary: float = 0.3,
    simulation_years: int = 20,
    added_people_rate: float = 0.6 * 0.37,
    retirment_age: int = 30,
    basic_retirment_strategy: bool = True,
):
    config = {
        "INFLATION_RATE": inflation_rate,
        "INSURANCE_FEE_FROM_SALARY": insurance_fee_from_salary,
        "SIMULATION_YEARS": simulation_years,
        "ADDED_PEAOPLE_RATE": added_people_rate,
        "RETIREMENTMENT_AGE": retirment_age,
        "BASIC_RETIRMENT_STRATEGY": basic_retirment_strategy,
    }
    mainClass = SimulationClass(config)
    mainClass.run()
    return mainClass.json_report()
