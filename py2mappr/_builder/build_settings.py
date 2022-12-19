import pandas as pd
from typing import Any, List, Dict
from py2mappr._layout import Layout

from py2mappr._core.config import ProjectConfig


def build_settings(
    snapshots: List[Layout] = [], playerSettings: ProjectConfig = {}
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
            "settings": playerSettings,
        },
        "snapshots": [snapshot.toDict() for snapshot in snapshots],
    }

    return settings
