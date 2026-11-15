import httpx
import pytest

import tarkov_dev

ID = "5644bd2b4bdc2d3b4c8b4572"
NAME = "AK-74N 5.45x39 assault rifle"
SHORT_NAME = "AK-74N"
DESCRIPTION = "AK-74N 5.45x39 assault rifle"
ICON_LINK = "https://assets.tarkov.dev/5644bd2b4bdc2d3b4c8b4572-icon.webp"
LINK = "https://tarkov.dev/item/ak-74n-545x39-assault-rifle"


ITEM = {
    "id": ID,
    "name": NAME,
    "shortName": SHORT_NAME,
    "description": DESCRIPTION,
    "iconLink": ICON_LINK,
    "link": LINK,
    "low24hPrice": 0,
    "high24hPrice": 0,
    "lastLowPrice": 0,
    "avg24hPrice": 0,
}


RESPONSE = {"data": {"items": [ITEM]}}


class FakeTarkovDev:
    def __init__(self):
        self.status_code = 200
        self.payload = RESPONSE
        self.error = None
        self.requests = []

    def post(self, url, headers=None, json=None, **kwargs):
        self.requests.append({"url": url, "headers": headers, "json": json})
        if self.error is not None:
            raise self.error
        return httpx.Response(self.status_code, json=self.payload, request=httpx.Request("POST", url))


@pytest.fixture
def api(monkeypatch):
    fake = FakeTarkovDev()
    monkeypatch.setattr(tarkov_dev.httpx, "post", fake.post)
    return fake


@pytest.fixture(autouse=True)
def run_in_tmp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
