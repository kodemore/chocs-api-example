from enum import IntEnum

from gata import DataClass


class Category(DataClass):
    id: int = 0
    name: str

    def __init__(self, name: str, id: int = 0):
        self.name = name
        self.id = id


class PetStatus(IntEnum):
    AVAILABLE = 1
    SOLD = 2


class Pet(DataClass):
    id: int = 0
    name: str
    category: Category
    status: PetStatus

    def __init__(self, name: str, category: Category, status: PetStatus, id: int = 0):
        self.id = id
        self.name = name
        self.category = category
        self.status = status
