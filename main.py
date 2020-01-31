from chocs import serve, router
from kink import di

from chinook import create_database
from chinook.middleware import check_json_request
from chinook.api import *

if __name__ == "__main__":
    create_database(di["database_path"], di["database_schema"])
    serve(check_json_request, router, host="localhost", port=8080)
