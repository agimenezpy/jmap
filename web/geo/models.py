# -*- coding: iso-8859-1 -*- 
from django.contrib.gis.db import models

class TipoVia(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.descripcion)

    class Meta:
        db_table = "tipo_via"
        verbose_name_plural = "Tipos de Vias de Transito"

class TipoLimite(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    
    def __unicode__(self):
        return "[%d] %s"  % (self.id, self.descripcion)
    
    class Meta:
        db_table = "tipo_limite"
        verbose_name_plural = u"Tipos de Límites Políticos"

class Limite(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.IntegerField(null=True)
    nombre = models.CharField(max_length=60)
    zorder = models.IntegerField(default=0)
    tipo = models.ForeignKey(TipoLimite)
    parent = models.ForeignKey("self", null=True)
    wiki_id = models.CharField(max_length=100,null=True)
    the_geom = models.PolygonField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "[%d] %s" % (self.gid, self.nombre)
    
    class Meta:
        db_table = "limite_politico"
        verbose_name_plural = u"Límites Políticos"

class Via(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    abrev = models.CharField(max_length=70)
    the_geom = models.MultiLineStringField()
    wiki_id = models.CharField(max_length=100,null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "via_transito"
        verbose_name_plural = "Vias de Transito"

class ViaTrazo(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.ForeignKey(Via,null=True)
    direccion = models.IntegerField(default=0)
    num_ini = models.SmallIntegerField(default=0)
    num_fin = models.SmallIntegerField(default=0)
    tipo = models.ForeignKey(TipoVia)
    zorder = models.IntegerField(default=0)
    prioridad = models.IntegerField(default=0)
    the_geom = models.LineStringField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "via_trazo"
        verbose_name_plural = "Trazos de Vias"

class TipoAOI(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.descripcion)
    
    class Meta:
        db_table = "tipo_area_interes"
        verbose_name_plural = "Tipos de Áreas de Interes"

class AreaInteres(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    zorder = models.IntegerField(default=0)
    tipo = models.ForeignKey(TipoAOI)
    wiki_id = models.CharField(max_length=100,null=True)
    the_geom = models.PolygonField()
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "area_interes"
        verbose_name_plural = "Áreas de Interes"

class TipoPOI(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.descripcion)
    
    class Meta:
        db_table = "tipo_punto_interes"
        verbose_name_plural = "Tipos de Puntos de Interes"

class PuntoInteres(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=90)
    zorder = models.IntegerField(default=0)
    tipo = models.ForeignKey(TipoPOI)
    wiki_id = models.CharField(max_length=100,null=True)
    the_geom = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "punto_interes"
        verbose_name_plural = "Puntos de Interes"
