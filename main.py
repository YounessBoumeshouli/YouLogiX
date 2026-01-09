from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI, Depends
from app.db.database import engine, Base, SessionLocal
import pytest

from app.db.database import engine, Base, SessionLocal
from routes.auth_routes import router as auth_router
from routes.client_routes import router as client_router
from routes.parcel_routes import router as parcel_router
from routes.logistic_manager_route import router as logistic_manager_router
from routes.delivery_man_route import router as delivery_man_router

from models.deliveryman_model import DeliveryManModel
from models.parcel_model import ParcelModel
from models.client_model import ClientModel
from models.logistic_manager_model import LogisticManagerModel


def setup_logging():
    logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")
    logger.add("logs/assignments.log", filter=lambda r: "ASSIGN" in r["message"])
    logger.add("logs/parcels.log", filter=lambda r: "PARCEL" in r["message"])
    logger.add("logs/CLIENT.log", filter=lambda r: "CLIENT" in r["message"])


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        logger.info("🌱 Seeding database...")
        DeliveryManModel(db).seed_delivery_men()
        ClientModel(db).seed_clients()
        ParcelModel(db).seed_parcels()
        LogisticManagerModel(db).seed_logistics_managers()
        logger.info("✅ Seeding complete.")
    except Exception as e:
        logger.error(f"❌ Seed error: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    print("🚀 Vérification de la connexion base de données...")
    exit_code = pytest.main(["tests/test_connection.py"])
    if exit_code != 0:
        logger.warning("⚠️ Connection tests failed. Check your .env configuration.")

    seed_database()

    logger.info("🚀 YouLogix API is up and running!")
    yield
    logger.info("🛑 App stopping...")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(client_router)
app.include_router(parcel_router)
app.include_router(logistic_manager_router)
app.include_router(delivery_man_router)


# @app.get("/admin/dashboard")
# async def admin_dashboard(
#     user: User = Depends(require_role("admin"))
# ):
#     return {"message": "Welcome admin"}

@app.get("/")
def read_root():
    return {"message": "FastAPI running"}