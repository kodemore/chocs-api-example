from dataclasses import dataclass
from typing import Optional

from .category import Category
from .pet_status import PetStatus


@dataclass()
class Pet:
    name: str
    category: Category
    status: PetStatus
    id: Optional[int] = 0
