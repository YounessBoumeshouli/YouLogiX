import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from main import app

# Create engine once
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from entities.client_entity import Client


@pytest.fixture
def valid_client(db_session):
    new_client = Client(
        first_name="Anas",
        last_name="Bennani",
        phone="0600000000",
        email="anas.test@example.com",
        password="hashed_password_123",
        address="Marrakech, Guiliz"
    )
    db_session.add(new_client)
    db_session.commit()
    db_session.refresh(new_client)
    return new_client
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # ONLY drop if the tables exist
    Base.metadata.drop_all(bind=engine, checkfirst=True) # Add checkfirst=True

@pytest.fixture
def db_session():
    # Start a transaction
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    # Rollback changes so the next test starts with a clean DB
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def override_db(db_session):
    def _get_db():
        yield db_session
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()