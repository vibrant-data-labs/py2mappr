from unittest import TestCase
import pandas as pd

from py2mappr._builder.build_dataset import build_datapoints


class BuildDatapointTestCase(TestCase):
    def test_string_text_is_converted_from_md(self):
        datapoint_dict = {
            "id": "test",
            "description": "This is a **test**.",
        }

        datapoint = pd.Series(datapoint_dict)
        dpAttribTypes = {"id": "string", "description": "string"}
        dpRenderTypes = {"id": "default", "description": "text"}
        expected = "<p>This is a <strong>test</strong>.</p>"

        result = build_datapoints(
            pd.DataFrame([datapoint], index=["description"]),
            dpAttribTypes,
            dpRenderTypes,
        )

        self.assertEqual(expected, result[0]["attr"]["description"])

    def test_string_default_not_converted_from_md(self):
        datapoint_dict = {
            "id": "test",
            "description": "This is a **test**.",
        }

        datapoint = pd.Series(datapoint_dict)
        dpAttribTypes = {"id": "string", "description": "string"}
        dpRenderTypes = {"id": "default", "description": "default"}
        expected = "This is a **test**."

        result = build_datapoints(
            pd.DataFrame([datapoint], index=["description"]),
            dpAttribTypes,
            dpRenderTypes,
        )

        self.assertEqual(expected, result[0]["attr"]["description"])
