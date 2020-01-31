import sqlite3

import pytest
from kink import di
from tests.utils import ApiClient

di[sqlite3.Connection] = lambda di: sqlite3.connect(":memory:")

# Setup database
connection = di[sqlite3.Connection]
cursor = connection.cursor()
with open(di["database_schema"], "r") as sql_schema_file:
    sql_schema = sql_schema_file.read()
    cursor.executescript(sql_schema)


@pytest.fixture()
def api_client() -> ApiClient:
    return ApiClient()
