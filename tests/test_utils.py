from chinook.utils import parse_query, QueryOperator, SortDirection
from chocs import QueryString


def test_parse_query() -> None:
    query = parse_query(
        QueryString("age[$gt]=12&name[$like]=test"),
        allow_fields={"age": True, "name": "login"},
    )

    assert len(query.operations) == 2
    assert query.operations[1].field == "login"
    assert query.operations[1].operator == QueryOperator.LIKE
    assert query.dumps() == "age[$gt]=12&name[$like]=test"


def test_parse_query_with_sort() -> None:
    query = parse_query(
        QueryString("age[$gt]=100&$sort=-age"), allow_fields={"age": True},
    )

    assert query.sort[0].field == "age"
    assert query.sort[0].direction == SortDirection.DESC
    assert query.dumps() == "age[$gt]=100&$sort=-age"


def test_parse_query_without_operators() -> None:
    query = parse_query(
        QueryString("age=10&name=Tom&$limit=15&$offset=5"), allow_fields=["age", "name"]
    )
    assert query.limit == 15
    assert query.offset == 5
    assert query.operations[0].field == "age"
    assert query.operations[0].operator == QueryOperator.EQUAL
    assert query.dumps() == "age=10&name=Tom&$offset=5&$limit=15"
