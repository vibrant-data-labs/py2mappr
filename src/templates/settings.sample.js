module.exports = {
  projName: 'name of the project',
  settings: {
    lastViewedSnap: 'snap-pgp3t7'
  },
  snapshots: [
    {
      id: 'snap-pgp3t7', // snapshot id
      descr: '', // html description for the snapshot
      snapName: 'Keyword Themes', // display name of the snapshot
      subtitle: '', // html text
      summaryImg: '', // html link to img or base64
      isEnabled: true,
      isDeleted: false,
      layout: {
        plotType: 'original', // 'original' | 'scatterplot' | 'grid' | 'geo'
        yaxis: "Clustered_1_Y",
        xaxis: "Clustered_1_X",
        settings: {
          drawNodes: true, // boolean - whether to draw or not nodes
          borderRatio: 0.15, // number - part of node which would be taken as a border
          bigOnTop: true, // boolean - whether to place bigger nodes on top
          nodeImageShow: true, // boolean - whether to show images on nodes 
          nodeImageAttr: 'Photo', // string (url) - name of attribute to render photo data for node
          nodeUnselectedOpacity: 0.25, // number - opacity of unselected nodes
          nodeHighlightRatio: 1.2, // number - size of highlighted node (relative to unselected state)
          nodeHighlightBorderOffset: 6, // number - offset of highlight border
          nodeHighlightBorderWidth: 1, // width of highlight border
          nodeSelectionRatio: 1.2, // same for the selection
          nodeSelectionBorderOffset: 0,
          nodeSelectionBorderWidth: 3,
          nodeSelectionDegree: 0, // number - degree of hover nodes

          nodePopSize: 10,
          nodePopImageShow: true,
          nodePopImageAttr: "Photo",
          nodePopShow: false,
          nodePopDelay: 1500,
          nodePopRepositionNeighbors: true, // boolean - reposition neighborgs node or not

          drawEdges: true, // boolean - whether to draw edges between nodes or not
          edgeDirectional: true, // boolean - is edge directional. if true, it will render as tapered
          edgeTaper: false, //boolean - draw taper for directed edges
          edgeTaperScale: 0.5, // number - thickness of tapered edge 
          edgeSaturation: 1, // number (0-1) - color saturation of edge
          edgeUnselectedOpacity: 0.2, //number (0-1) - opacity of unselected edges
          edgeDirectionalRender: "outgoing", // incoming | outgoing | all

          drawLabels: true, // boolean - show node labels
          drawGroupLabels: true, // boolean - show labels of colored groups (hides node labels unless zoomed in)
          labelColor: "#000000", // label color (default black)
          labelOutlineColor: "#ffffff", // label outline (default white)
          labelSize: "proportional", // label size proportional to node size
          labelScale: 1, // number - greater than 1 means the larger nodes have larger labels
          labelSizeRatio: 0.5, // number - max vs min label size when scaled
          defaultLabelSize: 12, // number - label size
          minLabelSize: 12, // number - minumum label size
          maxLabelSize: 16, // number - maxumum label size
          labelThreshold: 1, // ? I'm not sure what this does ? 
          labelMaxCount: 300, //  number - max labels to display
          labelDefaultShow: true, // ? I'm not sure what this does ? 
          labelAttr: "OriginalLabel", 
          labelHoverAttr: "OriginalLabel",
          labelDegree: 0, // ? I'm not sure what this does ? 
          labelOpacity: 1, // number (0-1) label opacity
          labelUnselectedOpacity: 0, // number (0-1) label unselected opacity

          zoomLock: true,
          panLock: true,

          maxZoomLevel: 10,
          minZoomLevel: -10,
          savedZoomLevel: 10, // valid for geo layout only

          zoomingRatio: 1.7, // configuration for zooming using +- buttons on screen
          mouseZoomDuration: 30000,

          xAxShow: false, // valid for scatterplot
          yAxShow: false, 
          xAxTickShow: false,
          yAxTickShow: false,
          xAxLabel: "",
          yAxLabel: "",
          xAxTooltip: "",
          yAxTooltip: "",
          invertX: false,
          invertY: true,
          scatterAspect: 0.5, // number (0-1) - higher number is wider than tall. 0.5 is square.

          mapboxMapID: 'mapbox/light-v10', // mapbox map id for geo layout
          
          nodeSizeStrat: "attr", // string - 'fixed' or any other value
          nodeSizeAttr: "Views Relative to Theme Avg", // attribute name to which nodes should be sized
          nodeSizeScaleStrategy: "linear", // 'linear' | 'log'
          nodeSizeScaleInvert: false,
          nodeSizeDefaultValue: 10,
          nodeSizeMin: 2,
          nodeSizeMax: 20,
          nodeSizeMultiplier: 0.5,

          nodeColorStrat: 'attr', // 'attr' | 'select' | 'fixed'
          nodeColorAttr: 'Keyword_Theme',
          nodeColorScaleStrategy: 'linear', // 'linear' | 'log'
          nodeColorScaleInvert: false,
          nodeColorScaleInvert: false,
          nodeColorScaleExponent: 2.5,
          nodeColorScaleBase: 10,
          nodeColorDefaultValue: "rgb(200, 200, 200)",
          nodeColorCycleCategoryColors: true,

          nodeColorPaletteNumeric: [ // for numeric attributes
            { col: '#ee4444'}
          ],
          nodeColorPaletteOrdinal: [ // for non numeric attributes
            { col: '#cc6600'}
          ],
          edgeSizeStrat: 'attr', // 'attr' | 'fixed'
          edgeSizeAttr: 'weight',
          edgeSizeScaleStrategy: 'linear', // 'linear' | 'log'
          edgeSizeScaleInvert: false,

          edgeSizeDefaultValue: 0.2,
          edgeSizeMin: 0.1,
          edgeSizeMax: 10,
          edgeSizeMultiplier: 0.4,

          edgeColorStrat: "gradient", // 'attr' | 'gradient' (gradient uses node colors as endpoints)
          edgeColorAttr: "OriginalColor", // color by attribute name (if edgeColorStrat = 'attr')
          edgeColorScaleStrategy: "linear",
          edgeColorScaleInvert: false,
          edgeColorScaleExponent: 2.5,
          edgeColorScaleBase: 10,
          edgeColorDefaultValue: "rgb(200,200,200)",
          edgeColorCycleCategoryColors: true,

          edgeColorPaletteNumeric: [ 
            { col: '#cceeee' }
          ],
          edgeColorPaletteOrdinal: [
            { col: '#cc6600'}
          ],

          isGeo: false,
        }
      }
    }
  ]
};