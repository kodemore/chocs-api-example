from abc import ABC
from sqlite3 import Connection, Cursor
from typing import Any, List, Tuple

from chinook.utils import Paginator, QueryOperator, SortDirection

QUERY_OPERATOR_TO_SQL_OPERATOR = {
    QueryOperator.EQUAL: "=",
    QueryOperator.GREATER_THAN: ">",
    QueryOperator.GREATER_OR_EQUAL: ">=",
    QueryOperator.LIKE: "LIKE",
    QueryOperator.LOWER_THAN: "<",
    QueryOperator.LOWER_OR_EQUAL: "<=",
}

SORT_DIRECTION_TO_SQL = {
    SortDirection.DESC: "DESC",
    SortDirection.ASC: "ASC",
}


class AbstractRepository(ABC):
    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, statement, *args) -> Cursor:
        cursor = self.connection.cursor()
        cursor.execute(statement, args)

        return cursor

    def commit(self):
        self.connection.commit()

    @classmethod
    def paginator_to_query(cls, paginator: Paginator) -> Tuple[str, str, List[Any]]:
        terms = ""
        data = []
        for operation in paginator.query.operations:
            terms += f"AND {operation.field} {QUERY_OPERATOR_TO_SQL_OPERATOR[operation.operator]} ?"
            data.append(operation.value)

        where = f" 1 {terms}"
        sort_options = []
        if paginator.query.sort:
            for sort_option in paginator.query.sort:
                sort_options.append(
                    f"{sort_option.field} {SORT_DIRECTION_TO_SQL[sort_option.direction]}"
                )

            where += "ORDER BY " + ", ".join(sort_options)

        limit = f" LIMIT {paginator.limit} OFFSET {paginator.offset}"

        return where, limit, data
