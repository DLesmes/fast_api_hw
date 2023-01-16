#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field,\
                    EmailStr,\
                    PaymentCardNumber,\
                    PositiveFloat,\
                    HttpUrl,\
                    SecretStr

from fastapi import FastAPI
from fastapi import status
from fastapi import Body,\
                    Query,\
                    Path,\
                    Form

app = FastAPI()

# Models

class HairColor(str, Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str = Field(..., 
                        min_length=1,
                        max_length=50,
                        regex='^[A-Za-z]*$',
                        example="Bogota"
                        )
    state: str = Field(..., 
                        min_length=1,
                        max_length=50,
                        regex='^[A-Za-z]*$',
                        example="Bogota"
                        )
    country: str = Field(..., 
                        min_length=1,
                        max_length=50,
                        regex='^[A-Za-z]*$',
                        example="Colombia"
                        )

class PersonOut(BaseModel): 
    first_name: str = Field(..., 
                            min_length=1,
                            max_length=50,
                            regex='^[A-Za-z]*$',
                            example="Miguel"
                            )
    last_name: str = Field(..., 
                            min_length=1,
                            max_length=50,
                            regex='^[A-Za-z]*$',
                            example="Torres"
                            )
    age: int = Field(...,
                    gt=0,
                    le=115,
                    example=25
                    )
    email: EmailStr = Field(...,
                            title="Person Email",
                            )
    credit_card: PaymentCardNumber = Field(...,
                                            title="Payment Card"
                                            )
    website: HttpUrl = Field(...,
                            title="linkedin profile"
                            )    
    hair_color: Optional[HairColor] = Field(default=None,
                                            example=HairColor.black
                                            )
    is_married: Optional[bool] = Field(default=None,
                                        example=False
                                        )
    weight: Optional[PositiveFloat] = Field(default=None,
                                            example=66
                                            )

class Person(PersonOut):
    password: SecretStr = Field(...,
                                title="Password",
                                min_length=8
                                )

    class Config: 
        schema_extra = {
            "example": {
                "first_name": "Jim",
                "last_name": "Rogers",
                "age": 21, 
                "email": "jim.rogers@mail.com",
                "credit_card" : "0000999988887777",
                "website" : "https://github.com/DLesmes",
                "hair_color": "blonde",
                "is_married": False,
                "weight" : "65",
                "password": "asdfghtyy"
            }
        }

class LoginOut(BaseModel): 
    username: str = Field(...,
                        max_length=20,
                        example="miguel2021"
                        )
    message: str = Field(default="Login Succesfully!")

@app.get(path="/",
        status_code=status.HTTP_200_OK
        ) # Called Path operation decorator
def home(): # Called path operation function
    return {"message": "Hello World"}


# Request and Response Body

@app.post(path="/person/new",
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED
        )
def create_person(person: Person = Body(...)): 
    return person

# Validaciones: Query Parameters

@app.get(path="/person/detail",
        status_code=status.HTTP_200_OK
        )
def show_person(
    name: Optional[str] = Query(None,
                                min_length=1,
                                max_length=50,
                                title="Person Name",
                                description="This is the person name. It's between 1 and 50 characters",
                                example="Rocío"),
    age: str = Query(...,
                    title="Person Age",
                    description="This is the person age. It's required",
                    example=25)): 
    return {name: age}

# Validaciones: Path Parameters

@app.get(path="/person/detail/{person_id}",
        status_code=status.HTTP_201_CREATED
        )
def show_person(
                person_id: int = Path(...,
                                    gt=0,
                                    example=123)
                ): 
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(path="/person/{person_id}",
        status_code=status.HTTP_204_NO_CONTENT
        )
def update_person(
    person_id: int = Path(...,
                        title="Person ID",
                        description="This is the person ID",
                        gt=0,
                        example=123
                        ),
    person: Person = Body(...),
    location: Location = Body(...)
    ): 
    results = person.dict()
    results.update(location.dict())
    return results
#forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
    )
def login(username: str = Form(...),
        password: str = Form(...)
        ): 
    return LoginOut(username=username)