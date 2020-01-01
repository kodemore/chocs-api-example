from petstore.db import create_database, di
from tempfile import gettempdir
from os import path, remove
from sqlite3 import connect


def test_create_database():
    tmp_filename = path.join(gettempdir(), "chocs-test-schema.db")
    if path.isfile(tmp_filename):
        remove(tmp_filename)

    create_database(tmp_filename, di["database_schema"])
    connection = connect(tmp_filename)
    cursor = connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = cursor.fetchall()
    assert len(table_list) - 1 == 5
