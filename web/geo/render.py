#!/usr/bin/python
from math import pi,cos,sin,log,exp,atan,tan
from subprocess import call
import sys, os
from mapnik import *
from django.contrib.gis.geos import fromstr
from web.settings import TILE_DIR
from PIL import Image
from StringIO import StringIO

ATRIB = Image.open(TILE_DIR + "atribucion.png")

DEG_TO_RAD = pi/180
RAD_TO_DEG = 180/pi
# Diametro de la tierra / un tile de 256 px
RESOLUTION_0 = 2*20037508.34 / 256

def minmax (a,b,c):
    a = max(a,b)
    a = min(a,c)
    return a

class GoogleProjection:
    def __init__(self,levels=18):
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        c = 256
        for d in range(0,levels):
            e = c/2;
            self.Bc.append(c/360.0)
            self.Cc.append(c/(2 * pi))
            self.zc.append((e,e))
            self.Ac.append(c)
            c *= 2

    def fromLLtoPixel(self,ll,zoom):
         d = self.zc[zoom]
         e = round(d[0] + ll[0] * self.Bc[zoom])
         f = minmax(sin(DEG_TO_RAD * ll[1]),-0.9999,0.9999)
         g = round(d[1] + 0.5*log((1+f)/(1-f))*-self.Cc[zoom])
         return (e,g)

    def fromPixelToLL(self,px,zoom):
         e = self.zc[zoom]
         f = (px[0] - e[0])/self.Bc[zoom]
         g = (px[1] - e[1])/-self.Cc[zoom]
         h = RAD_TO_DEG * ( 2 * atan(exp(g)) - 0.5 * pi)
         return (f,h)
    
    def forwardMercator(self, lon, lat):
        x = lon * 20037508.34 / 180;
        y = log(tan((90 + lat) * pi / 360)) / (pi / 180)
        y = y * 20037508.34 / 180
        return (x, y);

    def inverseMercator(self, x, y):
        lon = (x / 20037508.34) * 180
        lat = (y / 20037508.34) * 180
        lat = 180/pi * (2 * atan(exp(lat * pi / 180)) - pi / 2)
        return (lon, lat)

    def getCenter(self, ll0, ll1):
        dx = abs(ll0[0] - ll1[0])  / 2
        dy = abs(ll0[1] - ll1[1])  / 2
        return (ll0[0] + dx, ll0[1] + dy)

    def getLLCenter(self, center, zoom, w, h):
        resolution = RESOLUTION_0 / 2**zoom
        dx_2 = resolution*w / 2
        dy_2 = resolution*h / 2
        return ( center[0] -  dx_2, center[1] - dy_2, center[0] + dx_2, center[1] + dy_2)

    def mvCenterTo(self, center, zoom, w, h, gx, gy):
        resolution = RESOLUTION_0 / 2**zoom
        print resolution
        dx = resolution*w*gx
        dy = resolution*h*gy
        return ( center[0] +  dx, center[1] + dy)
    
    # Bbox corresponde a LOWER-LEFT , UPPER-RIGTH
    #                    minx, miny       maxx, maxy
    def getZoomBBox(self, ll0, ll1, w, h):
        resolution_x = (ll1[0] - ll0[0] )/w
        resolution_y = (ll1[1] - ll0[1])/h
        zx = log(RESOLUTION_0/resolution_x, 2)
        zy = log(RESOLUTION_0/resolution_y, 2)
        zoom = round(max(zx, zy))
        return int(zoom)

def render_tiles(geom, mapfile, tile_dir, minZoom=1,maxZoom=18, need_intersect=True):
    if not os.path.isdir(tile_dir):
         os.mkdir(tile_dir)

    gprj = GoogleProjection(maxZoom+1)
    m = Map(2 * 256,2 * 256)
    load_map(m,mapfile)
    prj = Projection("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over")
    bbox = geom.extent
    ll0 = (bbox[0],bbox[3])
    ll1 = (bbox[2],bbox[1])

    for z in range(minZoom,maxZoom + 1):
        px0 = gprj.fromLLtoPixel(ll0,z)
        px1 = gprj.fromLLtoPixel(ll1,z)
        for x in range(int(px0[0]/256.0),int(px1[0]/256.0)+1):
            for y in range(int(px0[1]/256.0),int(px1[1]/256.0)+1):
                p0 = gprj.fromPixelToLL((x * 256.0, (y+1) * 256.0),z)
                p1 = gprj.fromPixelToLL(((x+1) * 256.0, y * 256.0),z)
                
                # render a new tile and store it on filesystem
                c0 = prj.forward(Coord(p0[0],p0[1]))
                c1 = prj.forward(Coord(p1[0],p1[1]))

                g2 = fromstr("POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))" % (p0[0], p0[1], p0[0], p1[1], p1[0], p1[1], p1[0], p0[1], p0[0], p0[1]))
                
                if not need_intersect or geom.intersects(g2):
                    bbox = Envelope(c0.x,c0.y,c1.x,c1.y)
                    bbox.width(bbox.width() * 2)
                    bbox.height(bbox.height() * 2)
                    m.zoom_to_box(bbox)
    
                    # check if we have directories in place
                    zoom = "%s" % z
                    str_x = "%s" % x
                    str_y = "%s" % y
    
                    if not os.path.isdir(tile_dir + zoom):
                        os.mkdir(tile_dir + zoom)
                    if not os.path.isdir(tile_dir + zoom + '/' + str_x):
                        os.mkdir(tile_dir + zoom + '/' + str_x)
    
                    tile_uri = tile_dir + zoom + '/' + str_x + '/' + str_y + '.jpg'
    
                    exists= ""
                    im = Image(512, 512)
                    render(m, im)
                    view = im.view(128,128,256,256) # x,y,width,height
                    view.save(tile_uri,'jpeg')
    
                    bytes=os.stat(tile_uri)[6]
                    empty= ''
                    if bytes == 334:
                        empty = " Empty Tile "
                        os.unlink(tile_uri)

def static_map(lon, lat, zoom, width, height,response):
    gprj = GoogleProjection(19)
    ppr = gprj.forwardMercator(lon,lat)
    bbpr = gprj.getLLCenter(ppr,zoom,width,height)
    ll0 = gprj.inverseMercator(bbpr[0],bbpr[3])
    ll1 = gprj.inverseMercator(bbpr[2],bbpr[1])
    
    px0 = gprj.fromLLtoPixel(ll0,zoom)
    px1 = gprj.fromLLtoPixel(ll1,zoom)
    center = gprj.fromLLtoPixel((lon,lat),zoom)

    l_x = int(px0[0]/256.0)
    u_x = int(px1[0]/256.0)
    l_y = int(px0[1]/256.0)
    u_y = int(px1[1]/256.0)
    size = (int(u_x - l_x + 1)*256, (u_y - l_y + 1)*256)
    r_p = gprj.fromLLtoPixel(gprj.fromPixelToLL((l_x*256, l_y*256), zoom),zoom)
    c_x = int(center[0] - r_p[0])
    c_y = int(center[1] - r_p[1])
    im = Image.new("RGBA",size,(242,239,233,0))
    for y in range(l_y,u_y+1):
        for x in range(l_x,u_x+1):
            filename = "%s%d/%d/%d.jpg" % (TILE_DIR,zoom,x,y)
            if os.path.exists(filename):
                cx = (x - l_x)*256
                cy = (y - l_y)*256
                tile = Image.open(filename)
                im.paste(tile,(cx,cy))
                del tile
    size = (width/2,height/2)
    im = im.crop((c_x - size[0],c_y - size[1],c_x + size[0],c_y + size[1]))
    layer = Image.new("RGBA",(width,height),(0,0,0,0))
    layer.paste(ATRIB, (width - 250, height - 40))
    out = Image.composite(layer, im, layer)
    out.save(response,"JPEG",quality=90)
