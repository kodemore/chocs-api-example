from chocs import serve
from kink import di
import os

from chinook import create_database
from chinook.middleware import check_json_request
from chinook.api import *

if __name__ == "__main__":
    create_database(di["database_path"], di["database_schema"])
    serve(
        check_json_request,
        router,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
