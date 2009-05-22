from django.contrib.gis.maps.google import GoogleMap

def default(request):
    return google(request)

def google(request):
    x = -57.6061248779297
    y = -25.2940607556674
    if request.GET.has_key('x'):
        x = float(request.GET['x'])
    if request.GET.has_key('y'):
        y = float(request.GET['y'])
    g = GoogleMap(template="google-map.js", center = (x, y))
    return { "google" : g }