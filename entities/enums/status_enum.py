from enum import Enum

class EnumStatus(str, Enum):
    CREATED = 'CREATED'
    COLLECTED = 'COLLECTED'
    IN_STOCK = 'IN_STOCK'
    IN_TRANSIT = 'IN_TRANSIT'
    LIVRED = 'LIVRED'
