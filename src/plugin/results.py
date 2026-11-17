from typing import Iterator, List, Optional

from pyflowlauncher.api import open_url
from pyflowlauncher.result import Result
from pyflowlauncher.string_matcher import string_matcher

from tarkov_dev import Item


RUB_SYMBOL = "₽"


def format_price(price: Optional[int], symbol: str) -> str:
    if price is None:
        return "N/A"
    return f"{price:,}{symbol}"


def item_result(item: Item, score: int) -> Result:
    last_low_price = format_price(item["lastLowPrice"], RUB_SYMBOL)
    avg_24h_price = format_price(item["avg24hPrice"], RUB_SYMBOL)
    return Result(
        title=item["name"],
        subtitle=f"Lowest price: {last_low_price}, Avg last 24hr: {avg_24h_price}",
        icon=item["iconLink"],
        score=score,
    ).add_action(open_url(item["link"]))


def item_results(query: str, items: List[Item]) -> Iterator[Result]:
    for item in items:
        match = string_matcher(query, item["name"])
        if match.matched or query == "":
            yield item_result(item, int(match.score))
