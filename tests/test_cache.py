import json

import pytest

import src.cache as cache


def test_is_file_outdated(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.touch()
    assert not cache.is_file_outdated(file_path)


def test_is_file_outdated_missing_file(tmp_path):
    file_path = tmp_path / "test.txt"
    assert cache.is_file_outdated(file_path)


@pytest.fixture
def cache_run(tmp_path):
    cache_path = tmp_path / "test.json"
    payload = {"test": "test"}

    @cache.cache(freshness=0, cache_path=cache_path)
    def test_func():
        return payload

    return test_func


def test_cache(cache_run):
    assert cache_run() == {"test": "test"}


def test_cache_file(tmp_path, cache_run):
    cache_run()
    with open(tmp_path / "test.json") as f:
        assert json.load(f) == {"test": "test"}



