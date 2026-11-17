import asyncio
import json

import httpx

import tarky

from conftest import ITEM, LINK, NAME


def call(method, *params):
    return asyncio.run(tarky.plugin._event_handler.trigger_event(method, *params))


def test_query_returns_every_item_for_empty_search(api):
    response = call("query", "")

    assert [result["Title"] for result in response["Result"]] == [NAME]


def test_query_filters_by_name(api):
    api.payload = {"data": {"items": [ITEM, dict(ITEM, name="Salewa first aid kit")]}}

    response = call("query", "salewa")

    assert [result["Title"] for result in response["Result"]] == ["Salewa first aid kit"]


def test_query_result_opens_item_page(api):
    result = call("query", "ak")["Result"][0]

    assert result["JsonRPCAction"]["Method"] == "Flow.Launcher.OpenUrl"
    assert result["JsonRPCAction"]["Parameters"][0] == LINK


def test_query_response_is_json_serializable(api):
    json.dumps(call("query", "ak"))


def test_query_shows_api_error_as_result(api):
    api.status_code = 422
    api.payload = {"errors": ["GraphQL server unavailable. Try again later."]}

    response = call("query", "ak")

    assert len(response["Result"]) == 1
    assert response["Result"][0]["Title"] == "Could not load items from tarkov.dev"
    assert response["Result"][0]["SubTitle"] == "GraphQL server unavailable. Try again later."


def test_query_shows_graphql_error_message(api):
    api.payload = {"errors": [{"message": "Syntax Error: Expected Name, found )."}], "data": None}

    response = call("query", "ak")

    assert response["Result"][0]["SubTitle"] == "Syntax Error: Expected Name, found )."


def test_query_shows_network_error_as_result(api):
    api.error = httpx.ConnectError("Name or service not known")

    response = call("query", "ak")

    assert response["Result"][0]["Title"] == "Could not load items from tarkov.dev"
    assert response["Result"][0]["SubTitle"] == "Name or service not known"


def test_failed_request_is_not_cached(api):
    api.status_code = 422
    api.payload = {"errors": ["GraphQL server unavailable. Try again later."]}
    call("query", "ak")

    api.status_code = 200
    api.payload = {"data": {"items": [ITEM]}}

    assert [result["Title"] for result in call("query", "ak")["Result"]] == [NAME]
