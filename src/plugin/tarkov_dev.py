import logging
from typing import List, TypedDict

import httpx

from cache import cache


BASE_URL = "https://api.tarkov.dev/graphql"


logging.getLogger("httpx").setLevel(logging.WARNING)


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
        items() {
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
    return query(new_query).json()["data"]["items"]
