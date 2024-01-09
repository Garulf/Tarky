import src.plugin as plugin

from response import RESPONSE


def test_query(httpx_mock, monkeypatch):
    """Test that the query function returns a result response."""
    monkeypatch.setattr(plugin, "items", lambda: RESPONSE["data"]["items"])

    response = plugin.query("")
    assert response.keys() == {"result", "SettingsChange"}
    assert len(response["result"]) == 1
