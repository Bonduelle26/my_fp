import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AnimalCreateSchema(BaseModel):
    type: str
    name: str

class AnimalSchema(BaseModel):
    id: int
    type: str
    name: str

@app.post("/animals")
def create_animal(body: AnimalCreateSchema) -> AnimalSchema:
    return AnimalSchema(id=1, type=body.type, name=body.name)

@app.get("/animals/{id}")
def get_animal(id: int) -> AnimalSchema:
    return AnimalSchema(id=id, type="cat", name="Bob")

@app.get("/animals")
def get_all_animals(name: str | None = None, type: str | None = None) -> list[AnimalSchema]:
    
    return [
        AnimalSchema(id=1, type="cat", name="a"),
        AnimalSchema(id=2, type="cat", name="b"),
        AnimalSchema(id=3, type="cat", name="c")
    ]

@app.put("/animals/{id}")
def edit_animal(id: int, body: AnimalCreateSchema) -> AnimalSchema:
    return AnimalSchema(id=id, type=body.type, name=body.name)

@app.delete("/animals/{id}")
def delete_animal(id: int):
    return {"message": f"Animal with id {id} deleted"}

if name == "main":
    uvicorn.run(app)
