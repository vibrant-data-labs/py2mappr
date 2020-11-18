from typing import Any, List, Dict
import yaml
import copy


def load_templates(fname: str) -> Dict[str, Any]:
    try:
        templates: List[Dict] = []
        with open(f"src/templates/{fname}.yaml") as f:
            for project in yaml.load_all(f, Loader=yaml.FullLoader):
                templates.append(project)
        return templates[0]
    except FileNotFoundError as err:
        # no templates found.
        raise err


def merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    "merges b into a"
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            if isinstance(b[key], dict):
                a[key] = dict(b[key])  # copy
            else:
                a[key] = b[key]
    return copy.deepcopy(a)


if __name__ == "__main__":
    x = merge(
        {"a": 0, "b": 1, "c": {"c1": 1, "c2": 2, "c4": {"d": 0, "e": 1}}},
        {"a": 1, "c": {"c2": 22, "c3": 33, "c4": {"d": 6}}},
    )
    print(x)