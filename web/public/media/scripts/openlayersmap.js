var map;

var overlays = {};
var anyoverlay = false;

function olay_load() {
    map = new OpenLayers.Map("map", {controls:[]});
    map.addControl(new OpenLayers.Control.PanZoomBar());
    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.KeyboardDefaults());
    map.addControl(new OpenLayers.Control.Navigation());
    map.addControl(new OpenLayers.Control.NavToolbar());
    map.addControl(new OpenLayers.Control.Permalink($('permalink')));
    map.addControl(new OpenLayers.Control.Scale());
    map.addControl(new OpenLayers.Control.Attribution());
    map.viewPortDiv.style.width = "";
}
