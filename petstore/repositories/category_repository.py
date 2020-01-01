from petstore.repositories.abstract_repository import AbstractRepository
from petstore.entities import Category
from kink import inject
from sqlite3 import Cursor
from typing import Tuple


def _hydrate(cursor: Cursor, fields: Tuple[int, str]) -> Category:
    return Category(name=fields[1], id=fields[0])


@inject()
class CategoryRepository(AbstractRepository):
    def create(self, category: Category) -> None:
        cursor = self.execute("INSERT INTO categories(name) VALUES(?)", category.name,)

        category.id = cursor.lastrowid
        self.connection.commit()

    def get(self, id: int):
        cursor = self.execute(
            "SELECT category_id, name FROM categories WHERE category_id = ?", id
        )
        cursor.row_factory = _hydrate
        category = cursor.fetchone()
        cursor.close()

        return category
