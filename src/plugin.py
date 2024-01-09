from pyflowlauncher import Plugin
from pyflowlauncher.result import send_results

from results import item_results
from tarkov_dev import items

plugin = Plugin()


@plugin.on_method
def query(query: str):
    results = item_results(query, items())
    return send_results(results)
