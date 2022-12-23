from typing import List, Dict, Any
from .warn import warn


def any_id(datapoints: List[Dict[str, Any]], id: str):
    return any([datapoint["id"] == id for datapoint in datapoints])


def validate_source_target(
    links: List[Dict[str, Any]], datapoints: List[Dict[str, Any]]
):
    invalid_links = [
        link
        for link in links
        if not any_id(datapoints, link["source"])
        or not any_id(datapoints, link["target"])
    ]

    if len(invalid_links) > 0:
        warn(f"{len(invalid_links)} links have invalid source or target.")
