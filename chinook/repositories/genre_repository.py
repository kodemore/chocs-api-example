from sqlite3 import Cursor
from typing import Iterator, Tuple

from kink import inject

from chinook.entities import Genre
from chinook.repositories.abstract_repository import AbstractRepository
from chinook.utils import Paginator


def _hydrate(cursor: Cursor, fields: Tuple[int, str]) -> Genre:
    return Genre(id=fields[0], name=fields[1])


@inject()
class GenreRepository(AbstractRepository):
    def find_by_paginator(self, paginator: Paginator) -> Iterator[Tuple[int, Genre]]:
        where, limit, data = self.paginator_to_query(paginator)
        num_rows = self.execute(
            f"SELECT COUNT(genre_id) as num_rows FROM genres WHERE {where}", *data,
        ).fetchone()[0]

        paginator.total_items = num_rows
        query = f"SELECT genre_id, name FROM genres WHERE {where} {limit}"
        cursor = self.execute(query, *data)
        cursor.row_factory = _hydrate

        for entity in cursor:
            yield entity

        cursor.close()


__all__ = ["GenreRepository"]
