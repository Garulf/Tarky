from src.tarkov_dev import query, items

from response import RESPONSE


def test_query(httpx_mock):
    httpx_mock.add_response()

    """Test that the query function returns a response."""
    response = query("{ items { id } }")
    assert response.status_code == 200


def test_items(httpx_mock):
    httpx_mock.add_response(json=RESPONSE)

    """Test that the items function returns a list of items."""
    assert isinstance(items.__wrapped__(), list)
