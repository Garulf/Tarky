from pyflowlauncher import Plugin, Result

from results import item_results
from tarkov_dev import TarkovDevError, items

plugin = Plugin()


@plugin.on_method
def query(query: str):
    try:
        found = items()
    except TarkovDevError as error:
        return Result(
            title="Could not load items from tarkov.dev",
            subtitle=str(error),
            icon="icon.png",
        )
    return item_results(query, found)
