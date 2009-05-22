var map;

var overlays = {};
var anyoverlay = false;
function goSearch(obj) {
  var obj = new Ajax.Request('search.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            onComplete:function(request){$('progress').hide()},
            onLoading:function(request){$('search_results').hide();$('progress').show();},
            parameters:Form.serialize(obj)});
  return false;
}

function addGPoint(id, x, y, msg) {
    if (anyoverlay)
        map.clearOverlays();
    if (!overlays[id]) {
        overlays[id] = new GMarker(new GLatLng(y, x));
        overlays[id].bindInfoWindowHtml(msg);
        anyoverlay = true;
    }
    map.setCenter(overlays[id].getLatLng(), 17);
    map.addOverlay(overlays[id]);
    overlays[id].openInfoWindowHtml(msg);
    $('map').scrollTo();
}

function addGPolyline(id, detalle, points, xsw, ysw, xne, yne) {
    if (anyoverlay)
        map.clearOverlays();
    if (!overlays[id]) {
        i = 0;
        gpoints = [];
        points = points['coordinates']
        for (i = 0 ; i < points.length; i++){
            gpoints.push(new GLatLng(points[i][1], points[i][0]));
        }
        overlays[id] = new GPolyline(gpoints, "#0000FF", 10, 0.3);
        anyoverlay = true;
    }
    bounds = overlays[id].getBounds();
    map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds));
    map.addOverlay(overlays[id]);
    $('map').scrollTo();
    
    if (detalle) {
        var obj = new Ajax.Request('detail.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            parameters:{'detalle': detalle}});
    }
}

function addGPolylineE(id, stls, stlev, xsw, ysw, xne, yne) {
    if (anyoverlay)
        map.clearOverlays();
    if (!overlays[id]) {
        overlays[id] = new GPolyline.fromEncoded({
            color: "#0000FF",
            weight: 10,
            points: stls,
            levels: stlev,
            zoomFactor: 32,
            numLevels: 4,
            opacity: 0.3
        });
        anyoverlay = true;
    }
    bounds = new GLatLngBounds(new GLatLng(ysw, xsw), new GLatLng(yne, xne))
    map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds))
    try {
        map.addOverlay(overlays[id]);
    }
    catch (e) {}
    $('map').scrollTo();
}

function gmap_load(){
    if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById("map"));
        map.setCenter(new GLatLng(-25.2940607557, -57.6061248779), 4);
        //map.setUIToDefault();
        map.addControl(new GLargeMapControl());
        map.addControl(new GScaleControl());
        var otherOpts = { 
          buttonStartingStyle: {width:'16px',height:'16px',padding:0,margin:0,position:'absolute',border:'1px solid #000'},
          buttonHTML: "<img src='/media/images/dz.gif' />",
          buttonZoomingHTML: "<img src='/media/images/dza.gif' />",
          buttonZoomingStyle: {background:'yellow'}
        } 
        map.addControl(new DragZoomControl({}, otherOpts, {}), new GControlPosition(G_ANCHOR_TOP_LEFT, new GSize(7,7)));
        var myCopyright = new GCopyrightCollection("(c) ");
        myCopyright.addCopyright(new GCopyright('JMA', new GLatLngBounds(new GLatLng(-90,-180), new GLatLng(90,180)), 0,'&copy;2009 SIG Municipal <img src="/media/images/copyright.gif" width="34">'));
        var myTileLayer = new GTileLayer(myCopyright, 12, 17, {
              tileUrlTemplate: 'http://mt0.mapas.org.py/masu/{Z}/{X}/{Y}.jpg', 
              isPng:false,
              opacity:1
            });
        var custommapH = new GMapType([myTileLayer], G_NORMAL_MAP.getProjection(), "Asunción", G_NORMAL_MAP);
        map.getMapTypes().length = 0
        map.addMapType(custommapH);
        map.setMapType(custommapH);
        map.enableDoubleClickZoom();
        map.enableContinuousZoom();
        map.enableScrollWheelZoom();
    } else {
        alert("Sorry, the Google Maps API is not compatible with this browser.");
    }
}