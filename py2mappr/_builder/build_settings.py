from typing import Any, List, Dict
from py2mappr._layout import Layout

from py2mappr._core.config import ProjectConfig
from py2mappr._validation.validate_attributes import (
    validate_nodes,
    validate_links,
)
from py2mappr._validation.validate_settings import validate_settings
from ._utils import md_to_html


def build_settings(
    snapshots: List[Layout] = [],
    playerSettings: ProjectConfig = {},
    datapoints: List[Dict[str, Any]] = [],
    links: List[Dict[str, Any]] = [],
) -> Dict[str, Any]:
    """
    Builds the settings.json file for the project.

    Parameters
    ----------
    snapshots: List[Layout], optional. The list of layouts to be added to the
    project. The default is empty list.

    playerSettings: ProjectConfig, optional. The player settings to be added to
    the project. The default is empty dict.

    Returns
    -------
    Dict[str, Any]. The settings file data for the project.

    Exceptions
    ----------
    ValueError. If no snapshots are provided.
    """
    if len(snapshots) == 0:
        raise ValueError(
            "No snapshots found. Please add at least one snapshot to the project."
        )

    settings = {
        "dataset": {"ref": "id=dataset_ref_id"},
        "settings": {
            "theme": "light",
            "backgroundColor": "#ffffff",
            "labelColor": "#000000",
            "labelOutlineColor": "#ffffff",
            "selectionData": {"genCount": 0, "selections": []},
            "lastViewedSnap": "snal-id",
            "layouts": {},
        },
        "player": {
            "settings": {
                **playerSettings,
                "headerHtml": md_to_html(playerSettings["headerHtml"]),
                "modalDescription": md_to_html(
                    playerSettings["modalDescription"]
                ),
                "modalSubtitle": md_to_html(playerSettings["modalSubtitle"]),
            },
        },
        "snapshots": [
            {**snapshot.toDict(), "descr": md_to_html(snapshot.descr)}
            for snapshot in snapshots
        ],
    }

    for snapshot in settings["snapshots"]:
        validate_nodes(snapshot, datapoints)
        validate_links(snapshot, links)

    validate_settings(settings)

    return settings
