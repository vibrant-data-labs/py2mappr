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

## 3. The main method - `create_map`
    Args:
        datapointsPath (str): filepath for the datapoints
        linksPath (str): filepath for the edges
        datapointAttrPath (str): filespath for the datapoint attributes
        node_attr_map (Dict[str, str]): map of {required params: column-names} for the nodes
        link_attr_map (Dict[str, str]): map of {required params: column-names} for the links
        snapshots (List[Dict], optional): list of snapshots. Defaults to [].
        playerSettings (Dict[str, str], optional): settings to customize the player (info, theme etc). Defaults to {}
        outFolder (str, optional): name of the output folder. Defaults to "data_out".
    Return:
        None
    SideEffect:
        Writes the outFolder
        
## 4. Helper method to create snapshots - `create_snapshot`
    
    Args:
        name (str): snapshot title
        subtitle (str): snapshot subtitle
        summaryImg (str, optional): link to an image (ratio:110x80). Defaults to "".
        description (str, optional): description of snapshot. html ok.[description]. Defaults to "".
        layout_params (Dict, optional): see templates/snapshot.yaml. Defaults to {}.

    Returns:
        [Dict[str,Any]]: a snapshot object
