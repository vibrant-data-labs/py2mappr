# py2mappr
generate openmappr player from node and links .csv files

## 1. Installing packages
Only external libraries in use are: pandas and PyYAML. Install using requirements.txt

    pip install -r requirements.txt

## 2. Getting started
There are two samples in the top level directory of the repository

    ex_basic_map.py
    ex_map.py

Both of these scripts reads the contents of the top level `data_in` folder and outputs the `data_out` folder. The `data_out` is a self contained portable folder with all the resources necessary to render a map. To serve the map locally navigate to the `data_out` folder in a terminal shell and run the provided utility: 
    
    ./run_local.sh

or, you can simply run a python server at a desired port:

    python -m http.server <PORT_NUM>

## 3. The `data_in` folder

We need the following csv files in this folder to generate the map:

    nodes.csv - each row is a node in your network. The only required attributes per node - label, x, y
    link.csv - each row is a link. The required attributes per link - source, target, isDirectional
    datapointAttr.csv - each row is describes how mappr should treat a node attribute during render, search etc.
    
## 4. The `data_out` folder

This is the output of a py2mappr run. The following contents are generated:
    
    index.html              # entry point. has references to the openmappr player resources (js/css/images etc)
    data/
        nodes.json          # previously called datapoints.json
        links.json          # previously called networks.json
        settings.json       # previously called playerSetttings.json
    run_local.sh            # simple utility to run a local server
        
## 5. The main method - `create_map(..)`
    Args:
        datapointsPath (str):               filepath for the datapoints
        linksPath (str):                    filepath for the edges
        datapointAttrPath (str):            filespath for the datapoint attributes
        node_attr_map (Dict[str, str]):     map of {required params: column-names} for the nodes
        link_attr_map (Dict[str, str]):     map of {required params: column-names} for the links
        snapshots (List[Dict]):             list of snapshots. Optional. Defaults to [].
        playerSettings (Dict[str, str]):    settings to customize the player (info, theme etc). Optional.Defaults to {}
        outFolder (str):                    name of the output folder. Optional. Defaults to "data_out".
    Return:
        None
    SideEffect:
        Writes the outFolder
        
## 6. Helper method to create snapshots - `create_snapshot(..)`
    
    Args:
        name (str):                     snapshot title
        subtitle (str):                 snapshot subtitle
        summaryImg (str):               link to an image (ratio:110x80). Optional. Defaults to "".
        description (str):              description of snapshot. html ok.[description]. Optional. Defaults to "".
        layout_params (Dict):           see templates/snapshot.yaml. Optional. Defaults to {}.

    Returns:
        [Dict[str,Any]]: a snapshot object
