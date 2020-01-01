from petstore.repositories.abstract_repository import AbstractRepository
from petstore.entities import Pet
from kink import inject


@inject()
class PetRepository(AbstractRepository):
    
    def create(self, pet: Pet) -> None:
        cursor = self.execute(
            "INSERT INTO pets(name, status, category_id) VALUES(?, ?, ?)",
            pet.name,
            pet.status.value,
            pet.category.id
        )

        pet.id = cursor.lastrowid
        self.connection.commit()
