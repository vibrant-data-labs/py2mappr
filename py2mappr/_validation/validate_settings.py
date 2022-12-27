from typing import Dict
import jsonschema
import requests
from .warn import warn

def validate_settings(settings: Dict):
    # shared settings file
    settings_url = "https://raw.githubusercontent.com/vibrant-data-labs/openmappr-player/master/settings.schema.json"
    try:
        schema = requests.get(settings_url).json()

        validator = jsonschema.Draft4Validator(schema)

        errors = validator.iter_errors(settings)
        for error in errors:
            warn(f"[Invalid Schema]: {error.message} at {error.json_path}")
    except:
        warn(f"Unable to fetch settings schema at {settings_url}, skipping validation")
