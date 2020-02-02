from sqlite3 import Cursor
from typing import Iterator, Tuple

from kink import inject

from chinook.entities import Album
from chinook.repositories.abstract_repository import AbstractRepository
from chinook.utils import Paginator
from .artist_repository import ArtistRepository


@inject()
def _hydrate(
    cursor: Cursor, fields: Tuple[int, str, int], artist_repository: ArtistRepository
) -> Album:
    return Album(id=fields[0], title=fields[1], artist=artist_repository.get(fields[2]))


@inject()
class AlbumRepository(AbstractRepository):
    def find_by_paginator(self, paginator: Paginator) -> Iterator[Tuple[int, Album]]:
        where, limit, data = self.paginator_to_query(paginator)

        num_rows = self.execute(
            f'SELECT COUNT(album_id) as num_rows, artists.name as "artist.name" FROM albums JOIN artists ON artists.artist_id = albums.artist_id WHERE {where}',
            *data,
        ).fetchone()[0]

        paginator.total_items = num_rows
        query = f'SELECT album_id, title, artists.artist_id, artists.name as "artist.name" FROM albums JOIN artists ON artists.artist_id = albums.artist_id  WHERE {where} {limit}'
        cursor = self.execute(query, *data)

        cursor.row_factory = _hydrate

        for entity in cursor:
            yield entity

        cursor.close()
