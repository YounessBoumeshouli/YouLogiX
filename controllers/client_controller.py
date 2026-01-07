from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.client_model import ClientModel
from schemas.client_schema import ClientCreateSchema


class ClientController:

    def __init__(self, db: Session):
        self.model = ClientModel(db)

    # Create a client

    def create_client(self, payload: ClientCreateSchema):
        if self.model.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Client with this email already exists",
            )

        return self.model.create(**payload.model_dump())

    # Get a list of all clients

    def get_all_clients(self):
        return self.model.get_all()
    
    # Get a single client

    def get_client(self, client_id: int):
        client = self.model.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )
        return client
