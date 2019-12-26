import sqlite3
from os import path
from sqlite3 import Connection

from kink import inject

DB_PATH = path.join(path.dirname(__file__), "data/chocspetstore.db")
SCHEMA_PATH = path.join(path.dirname(__file__), "schema.sql")


def create_database(db_path: str, schema_path: str) -> None:
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    with open(schema_path, "r") as sql_schema_file:
        sql_schema = sql_schema_file.read()
        cursor.executescript(sql_schema)
        db.commit()
        db.close()


def setup_db(db_path: str, schema_path: str) -> None:
    if not path.isfile(db_path):
        create_database(db_path, schema_path)


@inject(db_path=DB_PATH)
def get_db(db_path: str) -> Connection:
    setup_db(db_path, SCHEMA_PATH)
    return sqlite3.connect(db_path)
