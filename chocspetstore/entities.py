from dataclasses import dataclass
from enum import IntEnum
from typing import List


class Category:
    id: int = 0
    name: str

    def __init__(self, name: str):
        self.name = name
        self.id = 0


class Photo:
    id: int = 0
    name: str
    url: str

    def __init__(self, name: str, url: str):
        self.id = 0
        self.name = name
        self.url = url


class PetStatus(IntEnum):
    AVAILABLE = 1
    SOLD = 2


class Pet:
    id: int = 0
    name: str
    category: Category
    photos: List[Photo]
    status: PetStatus

    def __init__(self, name: str, category: Category, status: PetStatus):
        self.id = 0
        self.name = name
        self.category = category
        self.status = status
        self.photos = []
