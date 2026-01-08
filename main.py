from fastapi import FastAPI
from app.db.database import engine, Base, SessionLocal
import pytest
import entities

### Models

from models.deliveryman_model import DeliveryManModel
from models.parcel_model import ParcelModel
from models.client_model import ClientModel

### Routes

from routes.client_routes import router as client_router
from routes.parcel_routes import router as parcel_router
from routes.logistic_manager_route import router as logistic_manager_router
from routes.delivery_man_route import router as delivery_man_router
from loguru import logger
app = FastAPI()
@app.on_event("startup")

def run_tests_on_startup():
    logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")
    logger.add("logs/assignments.log", filter=lambda r: "ASSIGN" in r["message"])
    logger.add("logs/parcels.log", filter=lambda r: "PARCEL" in r["message"])
    logger.info("This will be saved to the file!")
    print("🚀 Vérification de la connexion base de données...")
    exit_code = pytest.main(["tests/test_connection.py"])
    if exit_code != 0:
        print("❌ Les tests ont échoué. Vérifiez votre configuration .env")
    else:
        print("✅ Tests réussis !")
@app.on_event("startup")
def seeddelivery_men():
    Base.metadata.create_all(bind=engine)

    # 2. Open a manual session
    db = SessionLocal()
    try:
        print("🌱 Checking for seed data...")
        # Pass the actual session 'db' to the model
        model = DeliveryManModel(db)
        model.seed_delivery_men()
        c_model = ClientModel(db)
        c_model.seed_clients()
        p_model = ParcelModel(db)
        p_model.seed_parcels()
    except Exception as e:
        print(f"❌ Seed error: {e}")
    finally:
        # 3. Close it manually since 'get_db' isn't handling it here
        db.close()





app.include_router(client_router)
app.include_router(parcel_router)
app.include_router(logistic_manager_router)
app.include_router(delivery_man_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI running"}