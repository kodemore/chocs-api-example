from dataclasses import dataclass

from gata import PropertyMeta


@dataclass
class Genre:
    name: str
    id: int = 0

    class Meta:
        id = PropertyMeta(read_only=True)


__all__ = ["Genre"]
