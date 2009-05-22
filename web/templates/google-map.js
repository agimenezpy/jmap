{% extends "gis/google/js/google-map.js" %}
{% block functions %}
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

function resizeApp() {
    var offsetTop = 0;
    var mapElem = $("map");
    for (var elem = mapElem; elem; elem = elem.offsetParent)  {
        offsetTop += elem.offsetTop;
    }
    var height = getWindowHeight() - offsetTop - 32;
    if (height >= 0) {
        mapElem.style.height = height + "px";
        $("main").style.height =(height + 4) + "px";
        $("sub").style.height =(height + 4) + "px";
    }
}

function getWindowHeight() {
    if (window.self && self.innerHeight) {
        return self.innerHeight;
    }
    if (document.documentElement && document.documentElement.clientHeight) {
        return document.documentElement.clientHeight;
    }
    return 0;
}

function highlightFormElements() {
    // add input box highlighting
    addFocusHandlers($$("input"));
    addFocusHandlers($$("textarea"));
}

function addFocusHandlers(elements) {
    for (i=0; i < elements.length; i++) {
        if (elements[i].type != "button" && elements[i].type != "submit" &&
            elements[i].type != "reset" && elements[i].type != "checkbox" && elements[i].type != "radio") {
            if (!elements[i].getAttribute('readonly') && !elements[i].getAttribute('disabled')) {
                elements[i].onfocus=function() {this.style.backgroundColor='#ffd';this.select()};
                elements[i].onmouseover=function() {this.style.backgroundColor='#ffd'};
                elements[i].onblur=function() {this.style.backgroundColor='';}
                elements[i].onmouseout=function() {this.style.backgroundColor='';}
            }
        }
    }
}
{% endblock %}
{% block controls %}
map.addControl(new GLargeMapControl());
map.addControl(new GScaleControl());
{% endblock %}
{% block load_extra %}
var myCopyright = new GCopyrightCollection("(c) ");
myCopyright.addCopyright(new GCopyright('GD', new GLatLngBounds(new GLatLng(-90,-180), new GLatLng(90,180)), 0,'&copy;2008 Gu&iacute;a Digital <img src="/images/bg_head_top_logo.png" width="30">'));
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
{% endblock %}
