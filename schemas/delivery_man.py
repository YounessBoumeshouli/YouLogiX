# app/schemas/delivery_man.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from pydantic import ConfigDict
# Champs communs à toutes les opérations
class DeliveryManBase(BaseModel):
    address: str = Field(..., min_length=2, max_length=50)
    vehicule: str

# Utilisé pour la création (POST) - On peut ajouter des champs obligatoires ici
class DeliveryManCreate(DeliveryManBase):
    adress: str = Field(..., min_length=8)

# Utilisé pour la réponse (GET) - On ajoute l'ID et on active le mode ORM
class DeliveryManResponse(DeliveryManBase):
    id: int

    model_config = ConfigDict(from_attributes=True)