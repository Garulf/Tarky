import results

from conftest import ICON_LINK, ITEM, LINK, NAME

PRICE = 100_000


def test_format_price():
    assert results.format_price(PRICE, results.RUB_SYMBOL) == "100,000₽"


def test_item_result():
    result = results.item_result(ITEM, 0)

    assert result.title == NAME
    assert result.subtitle == "Lowest price: 0₽, Avg last 24hr: 0₽"
    assert result.json_rpc_action["Method"] == "Flow.Launcher.OpenUrl"
    assert result.json_rpc_action["Parameters"][0] == LINK
    assert result.icon == ICON_LINK
    assert result.score == 0


def test_item_results():
    generated_result = list(results.item_results("AK-74N", [ITEM]))[0]

    assert generated_result.title == NAME
    assert generated_result.subtitle == "Lowest price: 0₽, Avg last 24hr: 0₽"
    assert generated_result.json_rpc_action["Parameters"][0] == LINK
    assert generated_result.icon == ICON_LINK
    assert generated_result.score == 137


def test_item_results_skips_items_that_do_not_match():
    assert list(results.item_results("salewa", [ITEM])) == []
