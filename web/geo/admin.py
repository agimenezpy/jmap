# -*- coding: iso-8859-1 -*-
from django.contrib import admin
import django.contrib.gis.admin as admingis
from django.conf import settings
from web.geo.models import *

class ClaseBase:
    # Para WMS local 
    openlayers_url = '/media/scripts/OpenLayers.js'
    wms_name = u"Asunción"
    wms_url = '/wms/mapnik'
    wms_layer = 'default'
    map_template = 'gis/admin/jma.html'
    render_url = "render.xhr"
    
    def wiki_link(self, obj):
        if obj.wiki_id:
            return "<a href='%s/doku.php?id=%s' target='_blank'>%s</a>" % (settings.BASE_URL,obj.wiki_id, obj.wiki_id)
        else:
            return u"N/D"
    wiki_link.short_description = u"WikiID"
    wiki_link.allow_tags = True
    
    def link_render(self, obj):
        return "<a id='render_%s' href='/%s?id=%d' onclick='return showAddAnotherPopup(this);'>Dibujar Mapa</a>" % (obj.id, self.render_url, obj.id)
    link_render.short_description = u"Renderizado"
    link_render.allow_tags = True

class TipoViaAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'descripcion']

class TipoLimiteAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'descripcion']
    
class LimiteAdmin(ClaseBase,admingis.GeoModelAdmin):
    list_per_page = 15
    list_display = ['id', 'ref', 'nombre', 'tipo', 'wiki_link']
    search_fields = ['nombre']
    list_filter = ['tipo']
    
    fieldsets = (
        (None, {
            'fields' : ('ref','nombre','tipo','parent')
        }),
        (u'Publicación', {
            'fields' : ('wiki_id', 'zorder')
        }),
        (u'Ubicación Geográfica', {
            'fields' : ('the_geom',)
        })
    )

class ViaAdmin(ClaseBase,admingis.GeoModelAdmin):
    list_per_page = 15
    list_display = ['id', 'nombre', 'abrev', 'tipo', 'wiki_link', 'link_render']
    list_filter = ['tipo']
    search_fields = ['nombre']
    exclude = ["the_geom"]
    render_url = "render_via.xhr"
    
    fieldsets = (
        (None, {
            'fields' : ('nombre', 'abrev','tipo')
        }),
        (u'Publicación', {
            'fields' : ('wiki_id','zorder', 'prioridad')
        })
    )

class ViaTrazoAdmin(ClaseBase,admingis.GeoModelAdmin):
    list_display = ['id', 'ref', 'tipo', 'direccion', 'num_ini', 'num_fin']
    list_filter = ['tipo']
    list_per_page = 15
    search_fields = ['id','ref__nombre']
    raw_id_fields = ['ref']
    
    fieldsets = (
        (None, {
            'fields' : ('ref','tipo','direccion','num_ini','num_fin')
        }),
        (u'Publicación', {
            'fields' : ('zorder', 'prioridad')
        }),
        (u'Ubicación Geográfica', {
            'fields' : ('the_geom',)
        })
    )

class TipoAOIAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    list_per_page = 15

class AreaInteresAdmin(ClaseBase,admingis.GeoModelAdmin):
    list_display = ['id', 'nombre', 'tipo', 'wiki_link']
    list_per_page = 15
    list_filter = ['tipo']
    search_fields = ['nombre']
    
    fieldsets = (
        (None, {
            'fields' : ('nombre','tipo')
        }),
        (u'Publicación', {
            'fields' : ('wiki_id', 'zorder')
        }),
        (u'Ubicación Geográfica', {
            'fields' : ('the_geom',)
        })
    )

class TipoPOIAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    list_per_page = 15
    
class PuntoInteresAdmin(ClaseBase, admingis.GeoModelAdmin):
    list_display = ['id', 'nombre', 'tipo', 'wiki_link']
    list_per_page = 15
    list_filter = ['tipo']
    
    fieldsets = (
        (None, {
            'fields' : ('nombre','tipo')
        }),
        (u'Publicación', {
            'fields' : ('wiki_id', 'zorder')
        }),
        (u'Ubicación Geográfica', {
            'fields' : ('the_geom',)
        })
    )

admin.site.register(TipoVia, TipoViaAdmin)
admin.site.register(TipoLimite, TipoLimiteAdmin)
admin.site.register(Limite, LimiteAdmin)
admin.site.register(Via, ViaAdmin)
admin.site.register(ViaTrazo, ViaTrazoAdmin)
admin.site.register(TipoAOI, TipoAOIAdmin)
admin.site.register(AreaInteres, AreaInteresAdmin)
admin.site.register(TipoPOI, TipoPOIAdmin)
admin.site.register(PuntoInteres, PuntoInteresAdmin)