from sqlite3 import Cursor
from typing import Tuple

from chocspetstore.entities import Pet
from chocspetstore.entities import Photo
from .abstract_repository import AbstractRepository


def _hydrate(cursor: Cursor, row: Tuple[int, str]) -> Photo:
    return Photo(id=row[0], name=row[1], url=row[2])


class PhotosRepository(AbstractRepository):
    def fetch_for_pet(self, pet: Pet) -> None:
        cursor = self.execute(
            "SELECT pet_photo_id, name, url FROM pet_photos WHERE pet_id = ? LIMIT 1",
            pet.id,
        )
        cursor.row_factory = _hydrate
        pet.photos = cursor.fetchall()

    def save_for_pet(self, pet) -> None:
        self.execute("DELETE FROM pet_photos WHERE pet_id = ?", pet.id)
        for photo in pet.photos:
            cursor = self.execute(
                "INSERT INTO pet_photos('pet_id', 'name', 'url') VALUES(?, ?, ?)",
                pet.id,
                photo.name,
                photo.url,
            )
            photo.id = cursor.lastrowid
        self.commit()

