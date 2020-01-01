import sqlite3
from os import path
from sqlite3 import Connection

from kink import inject, di

di["database_path"] = path.join(path.dirname(__file__), "data/chocspetstore.db")
di["database_schema_path"] = path.join(path.dirname(__file__), "schema.sql")
di[Connection] = lambda di: sqlite3.connect(di["database_path"])
