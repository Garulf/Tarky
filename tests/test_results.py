import src.results as results

from response import ITEM, NAME, LINK, ICON_LINK

PRICE = 100_000


def test_format_price():
    """Test that the format_price function formats a price."""
    assert results.format_price(PRICE, results.RUB_SYMBOL) == "100,000₽"


def test_item_result():
    """Test that the item_result function returns a Result."""
    result = results.item_result(ITEM, 0)
    assert result.Title == NAME
    assert result.SubTitle == "Lowest price: 0₽, Avg last 24hr: 0₽"
    assert result.JsonRPCAction["method"] == "Flow.Launcher.OpenUrl"
    assert result.JsonRPCAction["parameters"][0] == LINK
    assert result.IcoPath == ICON_LINK
    assert result.Score == 0


def test_item_results():
    """Test that the item_results function generates results."""
    items = [ITEM]
    results_generator = results.item_results("AK-74N", items)
    generated_result = list(results_generator)[0]
    assert generated_result.Title == NAME
    assert generated_result.SubTitle == "Lowest price: 0₽, Avg last 24hr: 0₽"
    assert generated_result.JsonRPCAction["method"] == "Flow.Launcher.OpenUrl"
    assert generated_result.JsonRPCAction["parameters"][0] == LINK
    assert generated_result.IcoPath == ICON_LINK
    assert generated_result.Score == 137
