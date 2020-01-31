from dataclasses import dataclass

from gata import PropertyMeta

from .artist import Artist


@dataclass
class Album:
    title: str
    artist: Artist
    artist_id: int = 0
    id: int = 0

    class Meta:
        id = PropertyMeta(read_only=True)
        artist = PropertyMeta(read_only=True)
        artist_id = PropertyMeta(write_only=True)
