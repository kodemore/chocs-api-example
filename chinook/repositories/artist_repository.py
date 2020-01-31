from sqlite3 import Cursor
from typing import Iterator, Tuple

from kink import inject

from chinook.entities import Artist
from chinook.repositories.abstract_repository import AbstractRepository
from chinook.utils import Paginator


def _hydrate(cursor: Cursor, fields: Tuple[int, str]) -> Artist:
    return Artist(name=fields[1], id=fields[0])


@inject()
class ArtistRepository(AbstractRepository):
    def create(self, entity: Artist) -> None:
        cursor = self.execute("INSERT INTO artists(name) VALUES(?)", entity.name,)

        entity.id = cursor.lastrowid
        self.connection.commit()

    def delete(self, entity: Artist) -> None:
        self.execute("DELETE FROM artists WHERE artist_id = ?", entity.id)
        self.connection.commit()

    def update(self, entity: Artist) -> None:
        self.execute(
            "UPDATE artists SET name = ? WHERE artist_id = ?", entity.name, entity.id
        )
        self.connection.commit()

    def get(self, artist_id: int) -> Artist:
        cursor = self.execute(
            "SELECT artist_id, name FROM artists WHERE artist_id = ?", artist_id
        )
        cursor.row_factory = _hydrate
        entity = cursor.fetchone()
        cursor.close()

        if not entity:
            raise IndexError()

        return entity

    def find_by_paginator(self, paginator: Paginator) -> Iterator[Tuple[int, Artist]]:
        where, limit, data = self.paginator_to_query(paginator)

        num_rows = self.execute(
            f"SELECT COUNT(artist_id) as num_rows FROM artists WHERE {where}", *data
        ).fetchone()[0]

        paginator.total_items = num_rows

        cursor = self.execute(
            f"SELECT artist_id, name FROM artists WHERE {where} {limit}", *data
        )

        cursor.row_factory = _hydrate

        for entity in cursor:
            yield entity

        cursor.close()
