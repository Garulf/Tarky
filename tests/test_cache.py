import src.cache as cache


def test_is_file_outdated(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.touch()
    assert not cache.is_file_outdated(file_path)


def test_is_file_outdated_missing_file(tmp_path):
    file_path = tmp_path / "test.txt"
    assert cache.is_file_outdated(file_path)


def test_cache(tmp_path):
    cache_path = tmp_path / "test.txt"

    @cache.cache(freshness=0, cache_path=cache_path)
    def test_func():
        return {"test": "test"}

    assert test_func() == {"test": "test"}
