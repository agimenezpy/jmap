from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from web.geo.models import Via

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
            return calle(request)
        else:
            return render_to_response(page, query.detail(request), mimetype="application/javascript; charset=iso8859-1")
    except TemplateDoesNotExist:
        raise Http404()
    
def calle(request):
    params = request.REQUEST
    if params.has_key("query"):
        result = {}
        result["resultado"] = True
        nombre = params["query"].strip().replace(" "," & ")
        result["items"] = Via.objects.extra(where=["to_tsvector('spanish', nombre) @@ to_tsquery(%s)"], params=[nombre])
        result["count"] = len(result["items"])
        return render_to_response("calle.html", result, mimetype="application/javascript; charset=iso8859-1")
    else:
        return render_to_response("calle.html", {"resultado" : False, "count" : 0}, mimetype="application/javascript; charset=iso8859-1")
