from fastapi import FastAPI

app = FastAPI()


@app.get("/{item_id}")
def read_item(item_id: int):
    return {}
