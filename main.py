from fastapi import FastAPI

app = FastAPI()


@app.get("/") # Called Path operation decorator
def home(): # Called path operation function
    return {"message": "Hello World"}


# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)): 
    return person