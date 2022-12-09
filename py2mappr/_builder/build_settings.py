import pandas as pd
from typing import Any, List, Dict
from .utils import load_templates, merge
#from src.utils import load_templates, merge


def build_settings(snapshots: List[Dict] = [], playerSettings: Dict[str, Any] = {}) -> Dict[str, Any]:
    # load template - settings.yaml
    settings = load_templates("settings")

    # inject the snapshots
    if len(snapshots) > 0:
        print(f"\t- {len(snapshots)} snapshot found. adding to map.")
        settings = merge(settings, {"snapshots": snapshots})
    else:
        # if no snapshot defined load the default template and fix the size by and color by
        print(f"\t- no snapshot found. injecting default")
        default_snap = load_templates("snapshot")
        default_snap = merge(
            default_snap,
            {
                "layout": {
                    "plotType": "network",
                    "settings": {"nodeSizeStrat": "fixed", "nodeColorStrat": "fixed"},
                }
            },
        )
        settings = merge(settings, {"snapshots": [default_snap]})

    settings = merge(settings, {"player": {"settings": playerSettings}})

    return settings


if __name__ == "__main__":
    x = build_settings()
    print(x)
