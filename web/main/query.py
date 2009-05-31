from django.db import connection
from django.contrib.gis.geos import fromstr
#from guiadigital.site.geoutils import createEncodings
from web.geo.models import *
from re import compile, U, I, sub

fsm = compile(r"((?:\w+ ?)+)(/ ?(?:\w+ ?)+)?(, ?(?:\w+ ?)+)?(, ?(?:\w+ ?)+)?", U + I)
fsm2 = compile(r"((?:\w+ ?)+)( [0-9]+)$", U + I)
is_number = compile(r"[0-9]+")

def search(request):
    return isearch(request)

def detail(request):
    params = request.REQUEST
    result = {"item" : None }
    if params.has_key('detalle'):
        result["item"] = Detalle.objects.get(id=params['detalle'])
    return result

def isearch(request):
    start = 0
    limit = 15
    count = 0
    query = ""
    result = {"count" : 0, "items" : None}
    params = request.REQUEST
    
    if params.has_key("start"):
      start = params["start"]
    if params.has_key("limit"):
      limit = params["limit"]
    if params.has_key("query"):
      query = params["query"]
    
    query = fsm.search(query.strip())
    if query:
      nombre, inter, barrio, ciudad = map(simplify, query.groups())
      query = fsm2.search(nombre)
      if query:
        nombre, numero = query.groups()
    else:
        if params.has_key("nombre") and params["nombre"].length > 0:
            nombre = params["nombre"].replace("'", "''")
        if params.has_key("inter") and params["inter"].length > 0:
            inter = params["inter"].replace("'", "''")
        if params.has_key("barrio") and params["barrio"].length > 0 and is_number.search(params["barrio"]):
            barrio = int(params["barrio"])
        if params.has_key("zona") and params["zona"].length > 0 and is_number.search(params["zona"]):
            zona = int(params["zona"])
        if params.has_key("ciudad") and params["ciudad"].length > 0 and is_number.search(params["ciudad"]):
            ciudad = int(params["ciudad"])
    #result["items"] = mysearch(nombre, inter, barrio, zona, ciudad)
    #lookup.set_class(Calle)
    if nombre and not inter:
        result["items"] = Via.objects.filter(nombre__search=nombre).order_by('ref_id')[0:limit]
    result["count"] = len(result["items"])
    return result

def pgsearch(request):
    ctx = {}
    start = 0
    limit = 15
    count = 0
    query = ""
    if request.REQUEST.has_key('start'):
        start = request.REQUEST['start']
    if request.REQUEST.has_key('limit'):
        limit = request.REQUEST['limit']
    if request.REQUEST.has_key('query'):
        query = request.REQUEST['query']
    items = ""
    query = fsm.search(query.strip())
    if query:
        count = limit
        cursor = connection.cursor()
        nombre, inter, barrio, ciudad = query.groups();
        query = fsm2.search(nombre.strip())
        if query:
            nombre, numero = query.groups()
        
        if nombre and not inter:
            nombre = nombre.encode("LATIN-1").strip().replace(" ", "&")
            filtro = "WHERE idxFTI @@ to_tsquery('spanish', '" + nombre + "') "
            cursor.execute("SELECT COUNT(distinct id) FROM callemulti " + filtro)
            count = cursor.fetchone()[0]
            cursor.execute("SELECT gid, titulo, asewkb(transform(the_geom, 4326)) FROM callemulti " +
                           filtro +
                           "ORDER BY titulo LIMIT %s OFFSET %s " % (limit, start))
            ctx['items'] = map(construct, cursor.fetchall())
        else:
            nombre = nombre.encode("LATIN-1").strip().replace(" ", "&")
            inter = inter.encode("LATIN-1").strip().replace(" ", "&")
            filtro = "WHERE c1.idxFTI @@ to_tsquery('spanish', '" + nombre + "')"
            filtro += " AND c2.idxFTI @@ to_tsquery('spanish', '" + inter + "')"
            filtro += " AND intersects(c1.the_geom, c2.the_geom) = 't' "
            cursor.execute("SELECT COUNT(c1.id) FROM callemulti c1, callemulti c2 " + filtro)
            count = cursor.fetchone()[0]
            cursor.execute("SELECT c1.id, c2.id, c1.titulo, c2.titulo, asewkb(transform(intersection(c1.the_geom, c2.the_geom), 4326)) " +
                           "FROM callemulti c1, callemulti c2 " +
                           filtro +
                           "LIMIT %s OFFSET %s " % (limit, start))
            ctx['items'] = map(lambda (row): {'id' : "%s|%s" % (row[0], row[1]),
                                              'nombre' : "%s y %s" % (row[2], row[3]),
                                              'point' : fromstr(row[4])}, cursor.fetchall())
            ctx['inter'] = True
    ctx['count'] = count
    return ctx

def construct(row):
    lstr = fromstr(row[2]);
    #(estr, elevel) = createEncodings(lstr, 3)
    points = map(lambda p: list(p), lstr)
    result = {'id' : row[0],
    'nombre' : row[1],
    'polyline' : points,
    #'levels' : elevel,
    'bounds' : lstr.extent }
    return result

def simplify(str):
    if str:
        return sub("/|,", "", str).strip()
    else:
        return str