# -*- coding: iso-8859-1 -*- 
from django.contrib.gis.db import models

class TipoVia(models.Model):
    id = models.AutoField(primary_key=True)
    clave = models.CharField(u"Clave",max_length=40)
    descripcion = models.CharField(u"Descripci�n",max_length=60)
    
    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.descripcion)

    class Meta:
        db_table = "tipo_via"
        verbose_name = "Tipo de Vias de Transito"
        verbose_name_plural = "Tipos de Vias de Transito"
        ordering = ["id"]

class TipoLimite(models.Model):
    id = models.AutoField(primary_key=True)
    clave = models.CharField(u"Clave",max_length=40)
    descripcion = models.CharField(u"Descripci�n",max_length=60)
    
    def __unicode__(self):
        return u"[%d] %s"  % (self.id, self.descripcion)
    
    class Meta:
        db_table = "tipo_limite"
        verbose_name = u"Tipo de L�mites Pol�ticos"
        verbose_name_plural = u"Tipos de L�mites Pol�ticos"
        ordering = ["id"]

class Limite(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.IntegerField(u"Referencia",null=True)
    nombre = models.CharField(u"Nombre",max_length=60)
    zorder = models.IntegerField(u"Orden Z",default=0)
    tipo = models.ForeignKey(TipoLimite,verbose_name=u"Tipo de L�mite")
    parent = models.ForeignKey("self", verbose_name=u"Relacionado",null=True,blank=True)
    wiki_id = models.CharField(u"WikiID",max_length=100,null=True,blank=True)
    the_geom = models.PolygonField(u"Geometr�a")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "limite_politico"
        verbose_name = u"L�mite Pol�tico"
        verbose_name_plural = u"L�mites Pol�ticos"
        ordering = ["id"]

class Via(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(u"Nombre",max_length=100)
    abrev = models.CharField(u"Nombre Corto",max_length=70)
    tipo = models.ForeignKey(TipoVia, verbose_name=u"Tipo de V�a")
    zorder = models.IntegerField(u"Orden Z",default=0)
    prioridad = models.IntegerField(u"N�mero de Prioridad",default=0)
    wiki_id = models.CharField(u"WikiID",max_length=100,null=True,blank=True)
    the_geom = models.MultiLineStringField(u"Geometr�a",null=True,blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "via_transito"
        verbose_name = "Via de Transito"
        verbose_name_plural = "Vias de Transito"

class ViaTrazo(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.ForeignKey(Via,null=True,verbose_name=u"Referencia")
    direccion = models.IntegerField(u"Sentido",default=0)
    num_ini = models.SmallIntegerField(u"Inicio de Numeraci�n",default=0)
    num_fin = models.SmallIntegerField(u"Fin de Numeraci�n", default=0)
    tipo = models.ForeignKey(TipoVia, verbose_name=u"Tipo de V�a")
    zorder = models.IntegerField(u"Orden Z",default=0)
    prioridad = models.IntegerField(u"N�mero de Prioridad",default=0)
    the_geom = models.LineStringField(u"Geometr�a")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.ref)
    
    class Meta:
        db_table = "via_trazo"
        verbose_name = "Trazo de Via"
        verbose_name_plural = "Trazos de Vias"

class TipoAOI(models.Model):
    id = models.AutoField(primary_key=True)
    clave = models.CharField(u"Clave",max_length=40)
    descripcion = models.CharField(u"Descripci�n",max_length=60)
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.descripcion)
    
    class Meta:
        db_table = "tipo_area_interes"
        verbose_name = u"Tipo de �reas de Interes"
        verbose_name_plural = u"Tipos de �reas de Interes"
        ordering = ["id"]

class AreaInteres(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(u"Nombre",max_length=60)
    zorder = models.IntegerField(u"Orden Z",default=0)
    tipo = models.ForeignKey(TipoAOI,verbose_name=u"Tipo de �rea")
    area = models.IntegerField(u"�rea",default=0)
    wiki_id = models.CharField(u"WikiID",max_length=100,null=True,blank=True)
    the_geom = models.PolygonField(u"Geometr�a")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "area_interes"
        verbose_name = u"�rea de Interes"
        verbose_name_plural = u"�reas de Interes"

class TipoPOI(models.Model):
    id = models.AutoField(primary_key=True)
    clave = models.CharField(u"Clave",max_length=40)
    descripcion = models.CharField(u"Descripci�n",max_length=60)
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.descripcion)
    
    class Meta:
        db_table = "tipo_punto_interes"
        verbose_name = "Tipo de Puntos de Interes"
        verbose_name_plural = "Tipos de Puntos de Interes"
        ordering = ["id"]

class PuntoInteres(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(u"Nombre",max_length=90)
    zorder = models.IntegerField(u"Orden Z",default=0)
    tipo = models.ForeignKey(TipoPOI,verbose_name=u"Tipo de Punto")
    wiki_id = models.CharField(u"WikiID",max_length=100,null=True,blank=True)
    the_geom = models.PointField(u"Geometr�a")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u"[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "punto_interes"
        verbose_name = "Punto de Interes"
        verbose_name_plural = "Puntos de Interes"
