from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/sample")
def read_sample():
    return {"sample_data": "This is a sample JSON response"}
