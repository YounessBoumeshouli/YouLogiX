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
    
    
    def seed_clients(self):
        if self.db.query(Client).count() == 0:
            print("🌱 Initialisation des 10 clients...")
            for i in range(1, 11):
                new_man = Client(
                    first_name=f"Client {i}",
                    last_name=f"Client {i}",
                    email=f"client{i}@youlogix.com",
                    password="hashed_password_example",
                    address=f"{i} Rue de la Logistique - Rabat",
                    phone=f"06 549 9333{i}"
                )
                self.db.add(new_man)
            self.db.commit()
            print("✅ 10 clients insérés avec succès.")
        else:
            print("ℹ️ Les clients existent déjà, skipping seed.")