from pyflowlauncher import Plugin

from results import item_results
from tarkov_dev import items

plugin = Plugin()


@plugin.on_method
def query(query: str):
    return item_results(query, items())
