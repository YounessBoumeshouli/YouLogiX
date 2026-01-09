import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from entities import User
from auth.security import hash_password, create_access_token
from main import app
import uuid
# Create engine once
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from entities.client_entity import Client


@pytest.fixture
def valid_client(db_session):
    # Now uuid will work!
    unique_email = f"test_{uuid.uuid4().hex[:6]}@example.com"

    new_client = Client(
        first_name="Anas",
        last_name="Bennani",
        phone="0600000000",
        email=unique_email,
        password="hashed_password_123",
        address="123 Rue Marrakech",
        role="client"  # Ensure this matches your DB schema requirement
    )
    db_session.add(new_client)
    db_session.commit()
    db_session.refresh(new_client)
    return new_client
@pytest.fixture
def valid_logistic_manager(db_session):
    # Now uuid will work!
    unique_email = f"test_{uuid.uuid4().hex[:6]}@example.com"

    new_client = Client(
        first_name="Anas",
        last_name="Bennani",
        phone="0600000000",
        email=unique_email,
        password="hashed_password_123",
        address="123 Rue Marrakech",
        role="logistics_manager"  # Ensure this matches your DB schema requirement
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




@pytest.fixture
def logistics_manager_user(db_session):
    user = User(
        first_name="Test",
        last_name="Admin",
        email="manager@test.com",
        password=hash_password("password"),
        role="logistics_manager",
        phone="0000"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def logistics_manager_token(logistics_manager_user):
    return create_access_token(
        {"sub": str(logistics_manager_user.id), "role": 'logistics_manager'}
    )