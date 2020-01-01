from sqlite3 import Cursor
from typing import Tuple

from kink import inject

from chocspetstore.entities import Pet
from chocspetstore.entities import PetStatus
from .abstract_repository import AbstractRepository
from .category_repostiory import CategoryRepository
from .photos_repository import PhotosRepository


@inject(photos_repository=PhotosRepository(), category_repository=CategoryRepository())
def _hydrate(
    cursor: Cursor,
    row: Tuple[int, str],
    photos_repository: PhotosRepository,
    category_repository: CategoryRepository,
) -> Pet:
    pet = Pet(id=row[0], name=row[3], status=PetStatus(row[2]))
    pet.category = category_repository.get(row[1])
    photos_repository.fetch_for_pet(pet)

    return pet


class PetRepository(AbstractRepository):
    def get(self, pet_id: int) -> Pet:
        cursor = self.execute(
            "SELECT pet_id, category_id, status, name FROM pets WHERE pet_id = ? LIMIT 1",
            pet_id,
        )
        cursor.row_factory = _hydrate
        return cursor.fetchone()

    @inject(
        category_repository=CategoryRepository(), photos_repository=PhotosRepository()
    )
    def create(
        self,
        pet: Pet,
        category_repository: CategoryRepository,
        photos_repository: PhotosRepository,
    ) -> None:
        if not pet.category.id:
            category_repository.create(pet.category)

        photos_repository.save_for_pet(pet)
        cursor = self.execute(
            "INSERT INTO pets('category_id', 'name', 'status') VALUES(?, ?, ?)",
            pet.category.id,
            pet.name,
            pet.status.value,
        )
        pet.id = cursor.lastrowid
        self.commit()
