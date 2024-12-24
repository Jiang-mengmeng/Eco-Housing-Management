from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Decorators wrap functions to extend or modify behavior

@app.get("/")  # a FastAPI-specific decorator that registers the function directly below it as a handler for GET requests to the "/" route
async def root():  # create an asynchronous function : use async and await to handle tasks concurrently, improving performance for tasks that require waiting (like network requests)
    return {"Hello": "World"}

# python -m uvicorn serveur:app --reload
# curl --verbose "http://localhost:8000/"

@app.get("/etudiant/{id}/nom")
async def nom_etudiant(id):
    return id+"Paul"

# curl --verbose "http://localhost:8000/etudiant/32/nom"

@app.post("/items/")
async def create_item(item: Item):
    return item

# http://127.0.0.1:8000/docs#/