from petstore.repositories.abstract_repository import AbstractRepository
from petstore.entities import Category
from kink import inject


@inject()
class CategoryRepository(AbstractRepository):
    def create(self, category: Category) -> None:
        cursor = self.execute("INSERT INTO categories(name) VALUES(?)", category.name,)

        category.id = cursor.lastrowid
        self.connection.commit()
