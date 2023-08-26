from fastapi import FastAPI
from calculations.SimulationClass import SimulationClass

app = FastAPI()
mainClass = SimulationClass()


@app.get("/")
def read_item(skip: int = 0, limit: int = 10):
    mainClass.reset()
    mainClass.run()
    return mainClass.json_report()
