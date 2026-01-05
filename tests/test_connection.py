from sqlalchemy import text
from app.db.database import SessionLocal
import pytest

def test_database_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        value = result.scalar()

        assert value == 1
        print("\n✅ Connexion à la base de données réussie !")

    except Exception as e:
        pytest.fail(f"❌ Échec de la connexion à la base de données : {e}")
    finally:
        db.close()