from chocs import serve, router
from kink import di

from petstore import create_database
from petstore.middleware import check_json_request
import petstore.api

if __name__ == '__main__':
    create_database(di["database_path"], di["database_schema"])
    serve(check_json_request, router, host="localhost", port=8080)


