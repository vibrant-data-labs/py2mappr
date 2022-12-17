from typing import TypedDict
import pathlib as pl

class PublishOptions(TypedDict):
    path: pl.Path
    bucket_name: str
    url: str
