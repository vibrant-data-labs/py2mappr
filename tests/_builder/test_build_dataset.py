import pandas as pd

from py2mappr._builder.build_dataset import build_datapoints


def test_string_text_is_converted_from_md():
    datapoint_dict = {
        "id": "test",
        "description": "This is a **test**.",
    }

    datapoint = pd.Series(datapoint_dict)
    dpAttribTypes = {"id": "string", "description": "string"}
    dpRenderTypes = {"id": "default", "description": "text"}

    result = build_datapoints(
        pd.DataFrame([datapoint], index=["description"]),
        dpAttribTypes,
        dpRenderTypes,
    )

    expected = "<p>This is a <strong>test</strong>.</p>"
    assert expected == result[0]["attr"]["description"]


def test_string_default_not_converted_from_md():
    datapoint_dict = {
        "id": "test",
        "description": "This is a **test**.",
    }

    datapoint = pd.Series(datapoint_dict)
    dpAttribTypes = {"id": "string", "description": "string"}
    dpRenderTypes = {"id": "default", "description": "default"}

    result = build_datapoints(
        pd.DataFrame([datapoint], index=["description"]),
        dpAttribTypes,
        dpRenderTypes,
    )

    expected = "This is a **test**."
    assert expected == result[0]["attr"]["description"]
