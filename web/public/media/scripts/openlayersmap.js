var map;

var overlays = {};
var anyoverlay = false;
var geoParser

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

function addGPolyline(id, detalle, points, xsw, ysw, xne, yne) {
    if (anyoverlay) {
        map.layers[1].destroyFeatures();
        map.layers[2].clearMarkers();
    }
    
    if (!overlays[id]) {
        var sw = new OpenLayers.LonLat(xsw, ysw).transform(map.displayProjection, map.projection);
        var ne = new OpenLayers.LonLat(xne, yne).transform(map.displayProjection, map.projection);
        var geom = geoParser.read(points);
        var bounds = new OpenLayers.Bounds(sw.lon, sw.lat, ne.lon, ne.lat);
        overlays[id] = [geom, bounds];
        anyoverlay = true;
    }
    else {
        geom = overlays[id][0];
        bounds = overlays[id][1];
    }
    map.zoomToExtent(bounds);
    map.layers[1].setVisibility(false);
    map.layers[2].setVisibility(false);
    if (geom) {
        map.layers[1].addFeatures(geom);
    }
    map.layers[2].addMarker(new OpenLayers.Marker.Box(bounds));
    map.layers[2].setVisibility(true);
    map.layers[1].setVisibility(true);
    $('map').scrollTo();
    
    if (detalle && detalle != "None") {
        var obj = new Ajax.Updater('detalle', 'doku.php',
            {method:'get',
            asynchronous:true,
            parameters:{'id': detalle, 'do':'export_xhtmlbody'}});
    }
    else {
        $('detalle').update("");
    }
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
        numZoomLevels: 6,
        maxResolution: 156543.0339/Math.pow(2,12)
    };
    
    var asu = new OpenLayers.Layer.TMS("Asuncion","http://mt0.mapas.org.py/masu/", options);

    map.addLayer(asu);
    map.restrictedExtent = map.baseLayer.restrictedExtent;

    map.addControl(new OpenLayers.Control.PanZoomBar());
    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.Navigation());
    map.addControl(new OpenLayers.Control.ScaleLine());
    map.addControl(new OpenLayers.Control.Attribution());
    map.viewPortDiv.style.width = "";
    map.zoomToExtent(map.restrictedExtent)
    OpenLayers.Element.hide("msg");
    
    var control = new OpenLayers.Control();
    toggled = false;
    OpenLayers.Util.extend(control, {
        draw: function () {
            this.point = new OpenLayers.Handler.Point( control,
                {"done": function(evt) { alert(evt) }});
        }
    });
    
    var button = new OpenLayers.Control.Button({
        displayClass: "olControlPoint",
        title: "Información Contextual",
        trigger: function(evt) {
            if (!toggled) {
                this.activate()
                control.point.activate();
            }
            else {
                this.deactivate()
                control.point.deactivate();
            }
            toggled = !toggled;
            return true;
        }
    });
    
    var ms = new OpenLayers.Control.MouseDefaults(
            {displayClass: "olControlNavigation", title:'Posicionamiento con el Mouse.'});
    var panel = new OpenLayers.Control.Panel({defaultControl: ms, displayClass : "olControlNavToolbar"});
    panel.addControls([
        ms, 
        new OpenLayers.Control.ZoomBox(
            {displayClass : "olControlZoomBox", title:"Caja de Acercamiento: Realice click y arrastre para establecer la caja."}),
        button
    ]);
    map.addControl(panel);
    map.addControl(control);
    
    var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
    layer_style.fillOpacity = 0.2;
    layer_style.graphicOpacity = 0.5;
    layer_style.strokeColor = "#8B58F0";
    layer_style.fillColor = "#8B58F0";
    layer_style.strokeOpacity = 0.2;
    layer_style.strokeWidth = 6;
    var vectorLayer = new OpenLayers.Layer.Vector("Vector", {style: layer_style});
    map.addLayer(vectorLayer);
    var boxes  = new OpenLayers.Layer.Boxes("Boxes");
    map.addLayer(boxes);
    geoParser = new OpenLayers.Format.GeoJSON({externalProjection: map.displayProjection, internalProjection: map.projection});
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