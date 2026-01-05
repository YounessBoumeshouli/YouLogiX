from fastapi import FastAPI
from routes.client_routes import router as client_router

app = FastAPI()

app.include_router(client_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI running"}