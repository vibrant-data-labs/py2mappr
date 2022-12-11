import pandas as pd
from typing import Any, List, Dict
from py2mappr._layout import Layout

from py2mappr._core.config import ProjectConfig

def build_settings(snapshots: List[Layout] = [], playerSettings: ProjectConfig = {}) -> Dict[str, Any]:
    if len(snapshots) == 0:
        raise ValueError("No snapshots found. Please add at least one snapshot to the project.")

    settings = {
        'dataset': {
            'ref': 'id=dataset_ref_id'
        },
        'settings': {
            'theme': 'light',
            'backgroundColor': '#ffffff',
            'labelColor': '#000000',
            'labelOutlineColor': '#ffffff',
            'selectionData': {
                'genCount': 0,
                'selections': []
            },
            'lastViewedSnap': 'snal-id',
            'layouts': {},
            'displayExportButton': False #todo: add to config
        },
        'player': {
            'settings': playerSettings,
        },
        'snapshots': [snapshot.toDict() for snapshot in snapshots],
    }

    return settings

if __name__ == "__main__":
    x = build_settings()
    print(x)
