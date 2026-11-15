import graphql

import tarkov_dev

from conftest import ITEM


def test_query_posts_to_tarkov_dev(api):
    response = tarkov_dev.query("{ items { id } }")

    assert response.status_code == 200
    assert api.requests[0]["url"] == tarkov_dev.BASE_URL
    assert api.requests[0]["json"] == {"query": "{ items { id } }"}


def test_items_returns_item_list(api):
    assert tarkov_dev.items.__wrapped__() == [ITEM]


def test_items_requests_every_result_field(api):
    tarkov_dev.items.__wrapped__()

    sent = api.requests[0]["json"]["query"]
    for field in ITEM:
        assert field in sent


def test_items_query_is_valid_graphql(api):
    tarkov_dev.items.__wrapped__()

    graphql.parse(api.requests[0]["json"]["query"])
