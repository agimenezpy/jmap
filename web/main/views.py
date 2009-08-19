# -*- coding: iso-8859-1 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from web.geo.models import *
from django.contrib.gis.geos import fromstr
from django.db import connection
from django.contrib.auth.decorators import login_required
from web.geo.render import render_tiles,GoogleProjection
from django.conf import settings

def default(request, page):
    try:
        if page == "index.html":
            return render_to_response(page, mapa.default(request))
        else:
            return render_to_response(page)
    except TemplateDoesNotExist:
        raise Http404()

def xhr(request, page):
    try:
        if page == "search.xhr":
            #return render_to_response(page, query.search(request), mimetype="application/javascript; charset=iso8859-1")
            return calle_simple(request)
        elif page == "lugar.xhr":
            return lugar(request)
        elif page == "espacio.xhr":
            return espacio(request)
        elif page == "limite.xhr":
            return limite(request)
        elif page == "via.xhr":
            return via(request)
        elif page == "querybypoint.xhr":
            return querybypoint(request)
        elif page == "trazobypoint.xhr":
            return trazobypoint(request)
        elif page == "render_via.xhr":
            return render_via(request)
        else:
            raise TemplateDoesNotExist
    except TemplateDoesNotExist:
        raise Http404()
    
def calle_simple(request):
    params = request.REQUEST
    if params.has_key("query"):
        result = {}
        result["resultado"] = True
        nombre = params["query"].encode("latin-1").strip().replace(" "," & ")
        result["items"] = Via.objects.extra(where=["to_tsvector('spanish', nombre) @@ to_tsquery(%s)"], params=[nombre])
        result["count"] = len(result["items"])
        return render_to_response("calle.html", result, mimetype="application/javascript; charset=iso8859-1")
    else:
        return render_to_response("calle.html", {"resultado" : False, "count" : 0}, mimetype="application/javascript; charset=iso8859-1")

def lugar(request):
    params = request.REQUEST
    if params.has_key("nombre") and params.has_key("tipo") and len(params["nombre"]) > 0 and len(params["tipo"]) > 0:
        result = {}
        result["resultado"] = True
        nombre = params["nombre"].encode("latin-1").strip().replace(" "," & ")
        tipo = params["tipo"].strip()
        qs = PuntoInteres.objects.select_related()
        if tipo != "any":
            qs = qs.filter(tipo__clave__exact=tipo)
        result["items"] = qs.extra(where=["to_tsvector('spanish', nombre) @@ to_tsquery(%s)"], params=[nombre])
        result["count"] = len(result["items"])
        result["search_type"] = "lugar"
        return render_to_response("resultados.html", result, mimetype="application/javascript; charset=iso8859-1")
    else:
        return render_to_response("resultados.html", {"resultado" : False, "count" : 0, "search_type" : "lugar"}, mimetype="application/javascript; charset=iso8859-1")

def espacio(request):
    params = request.REQUEST
    if params.has_key("nombre") and params.has_key("tipo") and len(params["nombre"]) > 0 and len(params["tipo"]) > 0:
        result = {}
        result["resultado"] = True
        nombre = params["nombre"].encode("latin-1").strip().replace(" "," & ")
        tipo = params["tipo"].strip()
        qs = AreaInteres.objects.select_related()
        if tipo != "any":
            qs = qs.filter(tipo__clave__exact=tipo)
        result["items"] = qs.extra(where=["to_tsvector('spanish', nombre) @@ to_tsquery(%s)"], params=[nombre])
        result["count"] = len(result["items"])
        result["search_type"] = "espacio"
        return render_to_response("resultados.html", result, mimetype="application/javascript; charset=iso8859-1")
    else:
        return render_to_response("resultados.html", {"resultado" : False, "count" : 0, "search_type" : "espacio"}, mimetype="application/javascript; charset=iso8859-1")

def limite(request):
    params = request.REQUEST
    if params.has_key("nombre") and params.has_key("tipo") and len(params["nombre"]) > 0 and len(params["tipo"]) > 0:
        result = {}
        result["resultado"] = True
        nombre = params["nombre"].encode("latin-1").strip().replace(" "," & ")
        tipo = params["tipo"].strip()
        qs = Limite.objects.select_related()
        if tipo != "any":
            qs = qs.filter(tipo__clave__exact=tipo)
        result["items"] = qs.extra(where=["to_tsvector('spanish', nombre) @@ to_tsquery(%s)"], params=[nombre])
        result["count"] = len(result["items"])
        result["search_type"] = "limite"
        return render_to_response("resultados.html", result, mimetype="application/javascript; charset=iso8859-1")
    else:
        return render_to_response("resultados.html", {"resultado" : False, "count" : 0, "search_type" : "limite"}, mimetype="application/javascript; charset=iso8859-1")

def via(request):
    params = request.REQUEST
    if params.has_key("nombre") and params.has_key("entre") and params.has_key("barrio") and params.has_key("zona"):
        result = {}
        result["resultado"] = True
        nombre = params["nombre"].encode("latin-1").strip().replace(" "," & ")
        if len(params["entre"]) > 0:
            entre = params["entre"].encode("latin-1").strip().replace(" "," & ")
            cursor = connection.cursor()
            cursor.execute("""SELECT c1.id, c2.id, c1.abrev, c2.abrev, asewkb(intersection(c1.the_geom, c2.the_geom))
                           FROM via_transito c1, via_transito c2 
                           WHERE to_tsvector('spanish', c1.nombre) @@ to_tsquery(%s)
                             AND to_tsvector('spanish', c2.nombre) @@ to_tsquery(%s)
                             AND intersects(c1.the_geom, c2.the_geom) = 't'
                           """, [nombre, entre])
            result['items'] = map(lambda (row): {'id' : "%s%s" % (row[0], row[1]),
                                              'abrev' : "%s y %s" % (row[2], row[3]),
                                              'wiki_id' : None,
                                              'the_geom' : fromstr(row[4])}, cursor.fetchall())
        else:
            bound = None
            if params["barrio"] != "-1":
                bound = Limite.objects.filter(ref__exact=params["barrio"],tipo__clave__exact="barrio").get()
            elif params["zona"] != "-1":
                bound = Limite.objects.filter(ref__exact=params["zona"],tipo__clave__exact="zona").get()
            if bound:
                qs = Via.objects.filter(the_geom__contained=bound.the_geom)
            else:
                qs = Via.objects
            result["items"] = qs.extra(where=["to_tsvector('spanish', nombre) @@ to_tsquery(%s)"],params=[nombre])
        result["count"] = len(result["items"])
        result["search_type"] = "calle_"
        return render_to_response("calle.html", result, mimetype="application/javascript; charset=iso8859-1")
    else:
        return render_to_response("calle.html", {"resultado" : False, "count" : 0, "search_type" : "calle_"}, mimetype="application/javascript; charset=iso8859-1")

def querybypoint(request):
    params = request.REQUEST
    if params.has_key("point") and params.has_key("zoom") and len(params["point"]) > 0 and len(params["zoom"]) > 0:
        result = {}
        result["resultado"] = True
        point = params["point"]
        zoom = int(params["zoom"])
        if zoom < 3:
            if zoom == 0:
                tipo = "zona"
            else:
                tipo = "barrio"
            result["items"] = Limite.objects.select_related().filter(the_geom__contains=point,tipo__clave__exact=tipo)
        else:
            pnt = fromstr(point, srid=4326)
            result["items"] = Via.objects.select_related().filter(the_geom__dwithin=(pnt, 10*1.79866403673916e-05))
        result["count"] = len(result["items"])
        return render_to_response("querybypoint.html", result, mimetype="text/html; charset=iso8859-1")
    else:
        return render_to_response("querybypoint.html", {"resultado" : False, "count" : 0, "search_type" : "limite"}, mimetype="text/html; charset=iso8859-1")

def trazobypoint(request):
    params = request.REQUEST
    if params.has_key("point") and params.has_key("zoom") and len(params["point"]) > 0 and len(params["zoom"]) > 0 and int(params["zoom"]) > 2:
        result = {"id" : -1}
        point = params["point"]
        zoom = int(params["zoom"])
        pnt = fromstr(point, srid=4326)
        items = ViaTrazo.objects.filter(the_geom__dwithin=(pnt, 10*1.79866403673916e-05))[:1]
        result["id"] = items[0].id
        return render_to_response("trazobypoint.html", result, mimetype="text/html; charset=iso8859-1")
    else:
        return render_to_response("trazobypoint.html", {"id" : -1}, mimetype="text/html; charset=iso8859-1")

@login_required
def render_via(request):
    params = request.REQUEST
    ctx = {"title" : u"Generación de Cuadriculas", "is_popup":True}
    if params.has_key('id'):
        item = Via.objects.get(id=params["id"])
        render_tiles(item.the_geom,settings.TILE_MAPFILE,settings.TILE_DIR,14,17,False)
        ctx["messages"] = [u"Mapa Generado Exitosamente: %s" % item]
        return render_to_response("render.html", ctx)
    else:
        ctx["messages"] = [u"Sin Acciones Pendientes"]
        return render_to_response("render.html", ctx)