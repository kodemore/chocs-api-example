from abc import ABC
from sqlite3 import Connection
from sqlite3 import Cursor

from kink import inject

from chocspetstore.db import get_db


class AbstractRepository(ABC):
    @inject(connection=get_db)
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, statement, *args) -> Cursor:
        cursor = self.connection.cursor()
        cursor.execute(statement, args)

        return cursor

    def commit(self):
        self.connection.commit()
