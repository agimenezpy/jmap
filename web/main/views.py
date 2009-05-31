from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, RequestContext
from web.main import mapa, query

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
            return render_to_response(page, query.search(request), mimetype="application/javascript; charset=iso8859-1")
        else:
            return render_to_response(page, query.detail(request), mimetype="application/javascript; charset=iso8859-1")
    except TemplateDoesNotExist:
        raise Http404()
