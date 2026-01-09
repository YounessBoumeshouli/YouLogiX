from sqlalchemy.orm import Session
from loguru import logger

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
        logger.info(f"CLIENT: client {client.id} is created successfully")

        return client

    def seed_clients(self):
        if self.db.query(Client).count() == 0:
            print("🌱 Initialisation des 10 clients avec zones...")

            # Define the exact same zones as used for DeliveryMen
            city_zones = {
                "Marrakech": ["Menara", "Gueliz", "Medina", "Sidi Youssef"],
                "Casablanca": ["Anfa", "Maarif", "Ain Diab", "Sidi Moumen"],
                "Rabat": ["Agdal", "Hay Riad", "Hassan", "Yacoub El Mansour"]
            }
            cities = list(city_zones.keys())

            for i in range(1, 11):  # Creating 10 clients
                # Logic to cycle through cities and zones
                city_index = (i - 1) // 4 % len(cities)
                zone_index = (i - 1) % 4

                current_city = cities[city_index]
                current_zone = city_zones[current_city][zone_index]
                full_address = f"{current_city} {current_zone}"

                new_client = Client(
                    first_name=f"Client {i}",
                    last_name=f"Client {i}",
                    email=f"client{i}@youlogix.com",
                    password="hashed_password_example",
                    address=full_address,
                    phone=f"06 549 9333{i}"
                )
                self.db.add(new_client)

            self.db.commit()

        else:
            print("ℹ️ Les clients existent déjà, skipping seed.")