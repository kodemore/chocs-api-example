from enum import IntEnum

from gata import DataClass


class Category(DataClass):
    id: int = 0
    name: str

    def __init__(self, name: str):
        self.name = name
        self.id = 0


class PetStatus(IntEnum):
    AVAILABLE = 1
    SOLD = 2


class Pet(DataClass):
    id: int = 0
    name: str
    category: Category
    status: PetStatus

    def __init__(self, name: str, category: Category, status: PetStatus):
        self.id = 0
        self.name = name
        self.category = category
        self.status = status
        self.photos = []
