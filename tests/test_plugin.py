import asyncio
import json

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
