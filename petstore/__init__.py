import sqlite3
from os import path

from kink import di

di["database_path"] = path.join(path.dirname(__file__), "data/petstore.db")
di["database_schema"] = path.join(path.dirname(__file__), "data/schema.sql")
di[sqlite3.Connection] = lambda di: sqlite3.connect(di["database_path"])


def create_database(database_path: str, database_schema: str) -> None:
    if path.isfile(database_path):
        return None

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    with open(database_schema, "r") as sql_schema_file:
        sql_schema = sql_schema_file.read()
        cursor.executescript(sql_schema)
        connection.commit()
        connection.close()


__all__ = ["create_database"]
