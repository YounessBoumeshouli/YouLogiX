from sqlalchemy.orm import Session
from entities.client_entity import Client

class ClientModel:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Client).all()

    def get_by_id(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_by_email(self, email: str):
        return self.db.query(Client).filter(Client.email == email).first()

    def create(self, first_name: str, last_name: str, email: str, address: str, phone: str, password: str):
        client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            password=password
        )
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client