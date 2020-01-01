from sqlite3 import Cursor
from typing import List
from typing import Tuple

from kink import inject

from petstore.entities import Pet
from petstore.entities import PetStatus
from petstore.repositories.abstract_repository import AbstractRepository
from petstore.repositories.category_repository import CategoryRepository


@inject()
def _hydrate(cursor: Cursor, fields: Tuple[int, int, int, str], category_repository: CategoryRepository) -> Pet:
    return Pet(
        id=fields[0],
        name=fields[3],
        category=category_repository.get(fields[1]),
        status=PetStatus(fields[2]),
    )


@inject()
class PetRepository(AbstractRepository):
    def create(self, pet: Pet) -> None:
        cursor = self.execute(
            "INSERT INTO pets(name, status, category_id) VALUES(?, ?, ?)",
            pet.name,
            pet.status.value,
            pet.category.id,
        )

        pet.id = cursor.lastrowid
        self.connection.commit()

    def find(self, query: dict) -> List[Pet]:
        cursor = self.execute("SELECT pet_id, category_id, status, name FROM pets")
        cursor.row_factory = _hydrate
        return cursor.fetchall()
