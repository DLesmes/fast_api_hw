#uvicorn
import uvicorn

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
from fastapi import HTTPException
from fastapi import Body,\
                    Query,\
                    Path,\
                    Form,\
                    Header,\
                    Cookie,\
                    UploadFile,\
                    File

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

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Pages"]
) # Called Path operation decorator
def home(): # Called path operation function
    """
    Home page of the API

    This path returns the home page of the API.

    No parameters are required.
    """
    return {"message": "Hello World"}


# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary='Create Person in the app'
)
def create_person(person: Person = Body(...)):
    '''
    Create Person

    This path operation creates a person in the app and save the information in the database
    
    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status
    
    Returns a person model with first name, last name, age, hair color and marital status
    '''
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocío"
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
    )
):
    """Show Person
    
    This path operator that show the details of a person query

    - Query paramethers: 
        - **name (Optional[str])**: The person name that must have some conditions ( None, min_length=1, max_length=50, title="Person Name", description="This is the person name. It's between 1 and 50 characters", example="Rocío" )
        - **age (str, optional)**: The person age that must have some conditions ( ..., title="Person Age", description="This is the person age. It's required", example=25 )

    Returns a json: The person's name as the key and age as the values
    """
    return {name: age}

# Validaciones: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
    )
):
    """
    Show Person

    This path operation shows the person's ID in the app from the database.

    Parameters:
    - Path parameter:
        - **person_id: int** -> This is the person ID. It's required and must be greater than 0.

    Returns a JSON with the person's ID.
    """
    if person_id not in persons: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Persons"]
)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
): 
    """
    Update Person

    This path operation updates the person's information from the database.

    Parameters:
    - Path parameter:
        - **person_id: int** -> This is the person ID. It's required and must be greater than 0.
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color, is married, email, payment card number, favorite color and password.
        - **location: Location** -> A location model with city, state and country.

    Returns a JSON with the person's ID, its model and location.
    """
    results = person.dict()
    results.update(location.dict())
    return results

#forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=[
        "Persons",
        "Pages"
    ]
)
def login(
    username: str = Form(...),
    password: str = Form(...)
): 
    """
    User login

    This path operation allows you to login in the app.

    Parameters:
    - Request body parameter:
        - **username: str** -> This is the username to enter in the form. It's required.
        - **password: str** -> This is the password to enter in the form. It's required.

    Returns a JSON with the username and a message.
    """
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Pages"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """
    Contact

    This path operation allows the user to contact the company.

    Parameters:
    - user_agent: The browser that the user is using.
    - ads: The cookies that this website uses.
    - Request body parameter:
        - **first_name: str** -> This is the first name to enter in the form. It's required.
        - **last_name: str** -> This is the last name to enter in the form. It's required.
        - **email: EmailStr** -> This is the email to enter in the form. It's required.
        - **message: str** -> This is the message to enter in the form. It's required.

    """
    return user_agent

#files

@app.post(
    path='/post-image',
    tags=["Pages"]
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Post image

    This path operation allows you to post an image in the app to the database.

    Parameters:
    - Request body parameter:
        - **image: UploadFile** -> This is the image to upload. It's required.

    Returns a JSON with the image's name, format and size in kb.
    """
    return {
        'filename': image.filename,
        'format': image.content_type,
        'size(kb)': round(len(image.file.read()) / 1024, 2)
    }

if __name__ == "__main__":uvicorn.run(
        "__main__:app",
        host="localhost",
        port=8000,
        reload=True,
        workers=2
    )