{% extends "gis/admin/openlayers.js" %}

{% block base_layer %}new OpenLayers.Layer.WMS( "{{ wms_name }}", "{{ wms_url }}", {layers: '{{ wms_layer }}', format : 'image/png'},  opciones );{% endblock %}

{% block extra_layers %}
{{ module }}.map.restrictedExtent = geodjango_the_geom.map.baseLayer.restrictedExtent;
{{ module }}.map.zoomToExtent({{ module }}.map.restrictedExtent)
{% endblock %}

