from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from chocs import QueryString
from copy import deepcopy


class QueryOperator(Enum):
    GREATER_THAN = "$gt"
    GREATER_OR_EQUAL = "$gte"
    EQUAL = "$eq"
    LOWER_THAN = "$lt"
    LOWER_OR_EQUAL = "$lte"
    LIKE = "$like"


class SortDirection(Enum):
    ASC = "+"
    DESC = "-"


@dataclass()
class QueryOperation:
    query_field: str
    field: str
    operator: QueryOperator
    value: str


@dataclass()
class SortOperation:
    query_field: str
    field: str
    direction: SortDirection


class Query:
    def __init__(self, allow_fields: Dict[str, str]):
        self.operations: List[QueryOperation] = []
        self.sort: List[SortOperation] = []
        self.offset = 0
        self.limit = 0
        self.allow_fields = allow_fields

    def add_operation(
        self, field_name: str, operator: QueryOperator, field_value: str
    ) -> None:
        if field_name not in self.allow_fields:
            return
        self.operations.append(
            QueryOperation(
                field_name, self.allow_fields[field_name], operator, field_value
            )
        )

    def add_sort(self, field_name, direction: SortDirection):
        if field_name not in self.allow_fields:
            return
        self.sort.append(
            SortOperation(field_name, self.allow_fields[field_name], direction)
        )

    def dumps(self) -> str:
        query_string = ""
        for operation in self.operations:
            if operation.operator is QueryOperator.EQUAL:
                query_string += f"{operation.query_field}={operation.value}&"
            else:
                query_string += f"{operation.query_field}[{operation.operator.value}]={operation.value}&"

        if self.offset:
            query_string += f"$offset={self.offset}&"

        if self.limit:
            query_string += f"$limit={self.limit}&"

        if self.sort:
            query_string += "$sort="
            for sort in self.sort:
                query_string += f"{sort.direction.value}{sort.query_field}"
            query_string += "&"

        return query_string[0:-1]


def parse_sort(query_sort: str, query: Query) -> None:
    sort = query_sort.split(",")
    for sort_option in sort:
        direction = SortDirection.ASC
        sort_field = sort_option
        if sort_option[0] == "+":
            sort_field = sort_option[1:]
        elif sort_option[0] == "-":
            sort_field = sort_option[1:]
            direction = SortDirection.DESC

        query.add_sort(sort_field, direction)


def normalise_allow_fields(
    allow_fields: Union[List[str], Dict[str, Union[bool, str]]]
) -> Dict[str, str]:
    normalised = {}
    if isinstance(allow_fields, list):
        for field in allow_fields:
            normalised[field] = field
        return normalised

    if not isinstance(allow_fields, dict):
        raise ValueError("allow_fields must be either list or dict.")

    for field, value in allow_fields.items():
        if value is False:
            continue
        normalised[field] = field if value is True else value

    return normalised


def parse_query(
    query_string: QueryString,
    allow_fields: Union[List[str], Dict[str, Union[bool, str]]],
) -> Query:
    query = Query(normalise_allow_fields(allow_fields))
    if not allow_fields:
        return query

    for field, operations in query_string.items():
        if field == "$sort":
            parse_sort(str(operations), query)
            continue

        if field == "$limit":
            query.limit = int(operations)
            continue

        if field == "$offset":
            query.offset = int(operations)
            continue

        if not isinstance(operations, dict):
            query.add_operation(field, QueryOperator.EQUAL, operations)
            continue

        for operator, value in operations.items():
            try:
                operator = QueryOperator(operator)
                query.add_operation(field, operator, value)
            except ValueError:
                continue

    return query


class Paginator:
    def __init__(
        self,
        query_string: QueryString,
        uri: str,
        default_limit: int = 10,
        default_offset: int = 0,
        allow_fields: Union[List[str], Dict[str, Union[bool, str]]] = None,
    ):
        self.limit = int(query_string.get("$limit", default_limit))
        self.offset = int(query_string.get("$offset", default_offset))
        self.uri = uri
        self.query = parse_query(query_string, allow_fields)
        self.total_items = 0

    @property
    def hateos(self) -> dict:
        hateos = {
            "_links": [],
            "paging": {
                "total_items": self.total_items,
                "offset": self.offset,
                "limit": self.limit,
            },
        }
        self_query = self.query.dumps()
        if self_query:
            self_query = f"?{self_query}"
        hateos["_links"].append(
            {"rel": "self", "href": f"{self.uri}{self_query}", "method": "GET",}
        )

        if self.offset > 0:
            previous_offset = self.offset - self.limit
            previous_link = deepcopy(self.query)
            previous_link.offset = 0 if previous_offset < 0 else previous_offset
            previous_query = previous_link.dumps()
            if previous_query:
                previous_query = f"?{previous_query}"
            hateos["_links"].append(
                {
                    "rel": "previous",
                    "href": f"{self.uri}{previous_query}",
                    "method": "GET",
                }
            )

        if self.offset + self.limit < self.total_items:
            next_offset = self.offset + self.limit
            next_link = deepcopy(self.query)
            next_link.offset = next_offset
            next_query = next_link.dumps()
            if next_query:
                next_query = f"?{next_query}"
            hateos["_links"].append(
                {"rel": "next", "href": f"{self.uri}{next_query}", "method": "GET",}
            )

        return hateos
