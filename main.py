from fastapi import FastAPI

from models.deliveryman_model import DeliveryManModel
from models.client_model import ClientModel
from models.parcel_model import ParcelModel
from routes.client_routes import router as client_router
from routes.delivery_man_route import seed_delivery_men
from routes.parcel_routes import router as parcel_router
import pytest
from app.db.database import engine, Base, SessionLocal
import entities

app = FastAPI()

@app.on_event("startup")
def run_tests_on_startup():
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
        model_1 = DeliveryManModel(db)
        model_1.seed_delivery_men()

        model_2 = ClientModel(db)
        model_2.seed_clients()

        model_3 = ParcelModel(db)
        model_3.seed_parcels()
    except Exception as e:
        print(f"❌ Seed error: {e}")
    finally:
        # 3. Close it manually since 'get_db' isn't handling it here
        db.close()




app.include_router(client_router)
app.include_router(parcel_router)

@app.get("/")
def read_root():
    return {"message": "FastAPI running"}