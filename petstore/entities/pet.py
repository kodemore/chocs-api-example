from gata import DataClass

from .category import Category
from .pet_status import PetStatus


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
