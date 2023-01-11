#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(str, Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str
    state: str
    country: str

class Person(BaseModel): 
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        regex='^[A-Za-z]*$',
        example="Miguel"
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        regex='^[A-Za-z]*$',
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)


@app.get("/") # Called Path operation decorator
def home(): # Called path operation function
    return {"message": "Hello World"}


# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)): 
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None,
                                min_length=1,
                                max_length=50,
                                title="Person Name",
                                description="This is the person name. It's between 1 and 50 characters"),
    age: str = Query(...,
                        title="Person Age",
                        description="This is the person age. It's required")): 
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0)
): 
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
): 
    results = person.dict()
    results.update(location.dict())
    return results