import logging
from typing import Any, List, TypedDict

import httpx

from cache import cache


BASE_URL = "https://api.tarkov.dev/graphql"


logging.getLogger("httpx").setLevel(logging.WARNING)


class TarkovDevError(Exception):
    """The tarkov.dev API could not be reached or returned no data."""


class Item(TypedDict):
    """A Tarkov item."""

    id: str
    name: str
    shortName: str
    description: str
    iconLink: str
    link: str
    low24hPrice: int
    high24hPrice: int
    lastLowPrice: int
    avg24hPrice: int


def query(query: str) -> httpx.Response:
    """Query the Tarkov Dev API.

    Args:
        query (str): The query to send.

    Returns:
        httpx.Response: The response from the API.
    """
    headers = {"Content-Type": "application/json"}
    return httpx.post(
        BASE_URL, headers=headers, json={"query": query}
    )


@cache(freshness=0)
def items() -> List[Item]:
    """Query the Tarkov Dev API for all items.

    Returns:
        List[Item]: A list of items.
    """
    new_query = """
    {
        items {
            id
            name
            shortName
            description
            iconLink
            link
            low24hPrice
            high24hPrice
            lastLowPrice
            avg24hPrice
        }
    }
    """
    try:
        payload = query(new_query).json()
    except (httpx.HTTPError, ValueError) as error:
        raise TarkovDevError(str(error)) from error
    data = payload.get("data") if isinstance(payload, dict) else None
    if not data or data.get("items") is None:
        raise TarkovDevError(error_message(payload))
    return data["items"]


def error_message(payload: Any) -> str:
    errors = payload.get("errors") if isinstance(payload, dict) else None
    if not errors:
        return "Unexpected response from tarkov.dev"
    first = errors[0]
    if isinstance(first, dict):
        return str(first.get("message", first))
    return str(first)
