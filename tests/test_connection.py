from app.db.database import Base
from sqlalchemy import inspect
from tests.conftest import engine  # Import the test engine


def test_database_connection():
    
    Base.metadata.create_all(engine)

    # Use the inspector to see if tables were created in the test sqlite
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "users" in tables
    assert "clients" in tables