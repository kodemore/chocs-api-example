from gata import DataClass


class Category(DataClass):
    id: int = 0
    name: str

    def __init__(self, name: str, id: int = 0):
        self.name = name
        self.id = id
