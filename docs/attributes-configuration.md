# Attributes Configuration

This document describes the attributes configuration for the project. Each attribute is taken from the data frame and is used to create a field in the map.

Attributes are stored as a List of `AttributeConfig` objects in the Openmappr project.

All the attributes can be updated directly:

        project.attributes["My Attribute"]["renderType"] = "histogram"

Attributes have the following properties:
| Name | DataType| Default | Description|
|------|---------|---------|------------|
|id| str | - |The unique identifier for the attribute, matches the column name in the data frame.|
|title| str | - |The display title of the attribute, usually the same as the `id`.|
|visible| Boolean| `True` | Whether the attribute is visible in the project. If set to `False`, then the attribute is not used in the project.|
| visibleInProfile| Boolean | `True`|Whether the attribute is rendered in the profile panel.|
| searchable| Boolean| `True`|Whether the attribute is included in the search panel.|
|attrType| str `integer / string/ float/ liststring / timestamp / year` | - |The data type of the attribute|
|renderType| str `text / tag-cloud / tag_cloud_3 / tag-cloud_2 / wide-tag-cloud / histogram / horizontal-bars / video / picture / url` | - | The type of the renderer for the attribute|
|priority| str `high / low` | `high` |Important attributes are rendered in the filter panel as 'Data Filters' and the rest are rendered as 'Advanced Filters'. |
| axis| str `x / y / none / all`| `none` | Determines the axis of scatterplot/clustered-scatterplot where the attribute can be included ot the dropdown.|
| colorSelectable | Boolean | `False` | Whether the attribute can be included to the dropdown of selecting a color of nodes.|
| sizeSelectable | Boolean | `False` | Whether the attribute can be included to the dropdown of selecting a size of nodes. |


### Initial calculation

When the project is created, `py2mappr` performs an attempt to determine the type of the attribute and the renderer based on the data. The following rules are applied:

1. If column is of `number` type, i.e. `dataFrame[column].dtype in [np.number, np.int64]`, then it checks the values in the DataFrame.
    1. If all values fall in range [1800..2100], then the attribute is assigned `attrType = 'year'`.
    2. If all values fall in range [1000000000..9999999999] then attribute is assigned `attrType = 'timestamp'`.
    3. If all values can be divided by 1 without a remainder, then attribute is assigned `attrType = 'integer'`.
    4. Otherwise, attribute is assigned `attrType = 'float'`.
2. If at least one value has a `|` character, then attribute is assigned `attrType = 'liststring'`.
3. Otherwise, attribute is assigned `attrType = 'string'`.

The renderer is assigned based on the `attrType`:

1. If column has any numeric type (`attrType in ['integer', 'float', 'year', 'timestamp']`), then the renderer is assigned `renderType = 'histogram'`.
2. If column has `liststring` type, then it checks the values in the DataFrame.
    1. If there is more than 100 unique values, then the renderer is assigned `renderType = 'tag-cloud'`.
    2. If there is more than 80 unique values, then the renderer is assigned `renderType = 'tag_cloud_3'`.
    3. If there is more than 60 unique values, then the renderer is assigned `renderType = 'tag-cloud_2'`.
    4. If there is more than 40 unique values, then the renderer is assigned `renderType = 'wide-tag-cloud'`.
    5. Otherwise, the renderer is assigned `renderType = 'horizontal-bars'`.
3. Otherwise, the renderer is assigned `renderType = 'text'`.
