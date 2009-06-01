var map;

var overlays = {};
var anyoverlay = false;

function goSearch(obj) {
  var obj = new Ajax.Request('search.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            onComplete:function(request){OpenLayers.Element.hide('progress')},
            onLoading:function(request){OpenLayers.Element.hide('search_results');OpenLayers.Element.show('progress');},
            parameters:Form.serialize(obj)});
  return false;
}

function olay_load() {
    OpenLayers.Util.onImageLoadError = function() {
        this.src = "/media/images/404.png";
    }
    OpenLayers.IMAGE_RELOAD_ATTEMPTS = 5;
    OpenLayers.ImgPath = '/media/images/';
    map = new OpenLayers.Map("map", {
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34, 20037508.34, 20037508.34),
        controls:[]
    });
    
    var options = {
        isBaseLayer: true,
        buffer: 0,
        restrictedExtent: new OpenLayers.Bounds(
                            -57.6714897155762,-25.3689365386963, -57.5250053405762, -25.2249450683594
                        ).transform(map.displayProjection, map.projection),
        attribution: '&copy;2009 SIG Municipal <img src="/media/images/copyright.gif" width="34">',
        type: 'jpg',
        getURL: osm_getTileURL,
        displayOutsideMaxExtent: true,
        numZoomLevels: 5,
        maxResolution: 156543.0339/Math.pow(2,12)
    };
    
    var asu = new OpenLayers.Layer.TMS("Asuncion","http://mt0.mapas.org.py/masu/", options);

    map.addLayer(asu);
    map.restrictedExtent = map.baseLayer.restrictedExtent;

    map.addControl(new OpenLayers.Control.PanZoomBar());
    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.KeyboardDefaults());
    map.addControl(new OpenLayers.Control.Navigation());
    map.addControl(new OpenLayers.Control.NavToolbar());
    //map.addControl(new OpenLayers.Control.Permalink($('permalink')));
    map.addControl(new OpenLayers.Control.Scale());
    map.addControl(new OpenLayers.Control.Attribution());
    map.viewPortDiv.style.width = "";
    map.zoomToExtent(map.restrictedExtent)
    //map.setCenter(new OpenLayers.LonLat(-57.630001, -25.299999).transform(map.displayProjection, map.projection), 12)
    OpenLayers.Element.hide("msg");
}

function osm_getTileURL(bounds) {
    var res = this.map.getResolution();
    var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
    var y = Math.round((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
    var z = this.map.getZoom() + 12;
    var limit = Math.pow(2, z);

    if (y < 0 || y >= limit) {
        return OpenLayers.Util.getImagesLocation() + "404.png";
    } else {
        x = ((x % limit) + limit) % limit;
        return this.url + z + "/" + x + "/" + y + "." + this.type;
    }
}