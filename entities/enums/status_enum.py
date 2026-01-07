from enum import Enum

class EnumStatus(str, Enum):
    CREATED = 'CREATED'
    APPROVED = 'APPROVED'
    COLLECTED = 'COLLECTED'
    IN_STOCK = 'IN_STOCK'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'
