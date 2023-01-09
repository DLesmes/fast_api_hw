from fastapi import FastAPI

app = FastAPI()


@app.get("/") # Called Path operation decorator
def home(): # Called path operation function
    return {"message": "Hello World"}