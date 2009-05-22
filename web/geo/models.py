# -*- coding: iso-8859-1 -*- 
from django.contrib.gis.db import models

class Detalle(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    ref = models.CharField(max_length=30)
    descripcion = models.TextField()
    ubicacion = models.TextField()
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "detalle"
        verbose_name_plural = "Información del libro"

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
        verbose_name_plural = "Tipos de Límites Políticos"

class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    copyright = models.CharField(max_length=90)
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "autor"
        verbose_name_plural = "Autor de Datos"

class Limite(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.IntegerField(null=True)
    nombre = models.CharField(max_length=60)
    zorder = models.IntegerField(default=0)
    tipo = models.ForeignKey(TipoLimite)
    parent = models.ForeignKey("self", null=True)
    autor = models.ForeignKey(Autor)
    the_geom = models.PolygonField(srid=32721)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "[%d] %s" % (self.gid, self.nombre)
    
    class Meta:
        db_table = "limite_politico"
        verbose_name_plural = "Límites Políticos"

class Via(models.Model):
    id = models.AutoField(primary_key=True)
    ref_id = models.IntegerField(null=False)
    nombre = models.CharField(max_length=70)
    abrev = models.CharField(max_length=50)
    detalle = models.ForeignKey(Detalle,null=True)
    direccion = models.IntegerField(default=0)
    tipo = models.ForeignKey(TipoVia)
    zorder = models.IntegerField(default=0)
    prioridad = models.IntegerField(default=0)
    the_geom = models.LineStringField(srid=32721)
    objects = models.GeoManager()

    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "via_transito"
        verbose_name_plural = "Vias de Transito"        

class ViaTrazo(models.Model):
    id = models.AutoField(primary_key=True)
    ref_id = models.IntegerField(null=False)
    tipo = models.ForeignKey(TipoVia)
    zorder = models.IntegerField(default=0)
    prioridad = models.IntegerField(default=0)
    the_geom = models.LineStringField(srid=32721)
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
    autor = models.ForeignKey(Autor)
    the_geom = models.PolygonField(srid=32721)
    
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
    autor = models.ForeignKey(Autor)
    the_geom = models.PointField(srid=32721)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return "[%d] %s" % (self.id, self.nombre)
    
    class Meta:
        db_table = "punto_interes"
        verbose_name_plural = "Puntos de Interes"
    
#class ViaLibro(models.Model):
#    via = models.IntegerField(null=False)
#    libro = models.IntegerField(null=False)
    
#    def __unicode__(self):
#        return "(%d, %d)" % (self.via, self.libro)
#    
#    class Meta:
#        db_table = "via_libro"
#        verbose_name_plural = "Via por libro"
#    