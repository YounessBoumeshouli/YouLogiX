from fastapi import FastAPI
from routes.client_routes import router as client_router
import pytest

app = FastAPI()
@app.on_event("startup")
def run_tests_on_startup():
    print("🚀 Vérification de la connexion base de données...")
    exit_code = pytest.main(["tests/test_connection.py"])
    if exit_code != 0:
        print("❌ Les tests ont échoué. Vérifiez votre configuration .env")
    else:
        print("✅ Tests réussis !")

app.include_router(client_router)
app.include_router(client_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI running"}