#!/usr/bin/python
# -*- coding: iso8859-1 -*-
import os
from re import match, compile, findall, split, sub

class Barrio:
    def __init__(self):
        self.id = 0
        self.nombre = ""
        self.referencia = ""
        self.descripcion = ""
        self.ubicacion = ""
        self.superficie = ""
        self.poblacion = ""
        self.tmpl = """
====== %(nombre)s ======

=====  Referencia =====

%(referencia)s

===== Descripción =====

%(descripcion)s

===== Ubicación =====

%(ubicacion)s

^  Superficie  |  %(superficie)s  |
^  Población  |  %(poblacion)s  |

"""

    def __str__(self):
        return "Nombre: %s (%s)\nRef: %s\nDescripci\xf3n: %s\nUbicaci\xf3n: %s\nSuperficie: %s\nPoblación: %s\n" % (self.nombre, self.id, self.referencia, self.descripcion, self.ubicacion, self.superficie, self.poblacion)

    def __repr__(self):
        return self.__str__()
    
    def save(self, nombre):
        genid = self.nombre_id()
        fd = open("../dokuwiki/data/pages/barrio/%s.txt" % genid, "w")
        fd.write(self.convert(self.tmpl % self))
        fd.close()
        return "%d barrio:%s" % (self.id, genid)
    
    def __getitem__(self, strk):
        if hasattr(self, strk):
            return getattr(self, strk)
        else:
            return ""
        
    def nombre_id(self):
        clean = reduce(lambda x,y: x + " " + y, filter(lambda i: not match("^(DE|LA|LAS|DEL)$", i), sub(",|\.|'", "", self.nombre).split()))
        result = reduce(lambda x,y: x + "_" + y, clean.decode("latin-1").lower().split()[0:2]).encode("latin-1") + "." + str(self.id)
        remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "n", "ü" : "u"}
        for k, v in remp.iteritems():
            result = result.replace(k, v)
        return result
    
    def convert(self, strT):
        return strT.decode("latin-1").encode("UTF-8")

class Barrios:
    def __init__(self):
        self.reg = []
        self.remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "Ñ"}
        fd = open("barrios.dat", "r")
        try:
            while True:
                ident, nombre = fd.next().strip().split(" ", 1)
                self.reg.append((int(ident), nombre))
        except StopIteration:
            pass
        fd.close()

    def getId(self, nombre):
        nombre = nombre.decode("latin-1").lower().encode("latin-1")
        for k, v in self.remp.iteritems():
            nombre = nombre.replace(k, v)
        nombre = nombre.upper()
        for tupla in self.reg:
            if nombre.find(tupla[1]) != -1:
                return tupla[0]
    
    def link(self, value):
        id = self.getId(value)
        if id:
            return "[[barrio:%d|%s]]" % (id, value)
        else:
            return None

def isValid(str):
    return len(str) > 1 and not match("Asunci\xf3n y sus calles.*$", str) and not match("^  +Osvaldo Kallsen.*$", str) and str != "CH"

def unpack(list):
        first = ""
        result = ""
        for i in list:
            if i:
                result += first + i
                first = ", "
        return result

if __name__ == '__main__':
    comp = [compile("^[A-ZÁÉÍÓÚÑ0-9][A-ZÁÉÍÓÚÑ0-9'\.].*\((Resoluci\xf3n|Ordenanza|Decreto).*\)(\.)?$|^[A-WY-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\.].*(\.)?"),
            compile("^Ubicaci\xf3n:.*"),
            compile("^Superficie.*:.*"),
            compile("^Poblaci\xf3n.*")]
    categoria = {0 : "Barrio", 1 : "Ubicacion", 2 : "Superficie", 3 : "Poblacion", 4 : "otro"}
    b = Barrio()
    barrios = Barrios()
    asoc = open("barrio_asoc.txt", "w")
    last = ""
    #1680 2198 Barrios de Asuncion BYTES 61719
    lno = 1680
    nombre = "Asuncion007-Plazas_Otros.txt"
    print "Procesando " + nombre
    f = open(nombre, 'r')
    f.seek(60538)
    while (lno < 2198):
        num = 4;
        linea = f.next().strip()
        for i in range(0, 4):
            if (comp[i].match(linea)):
                num = i
                break
        if (isValid(linea)):
            actual = categoria.get(num)
            if (actual == "Barrio"):
                if (len(last) > 0):
                    asoc.write(b.save(nombre) + "\n")
                    b.__init__()
                par = linea.split("(")
                b.nombre = par[0].replace("[", "(").replace("]", ")").strip()
                #if match(".*([A-Z0-9ÁÉÍÓÚ]| )\.$", b.nombre):
                #    print b.nombre
                #    b.nombre = b.nombre[:-1]
                b.nombre = b.nombre.replace("´", "'")
                if (len(par) == 2):
                    b.referencia = par[1].replace(")", "").replace(".", "")
                b.id = barrios.getId(b.nombre)
                if not b.id:
                    b.id = -1
                    print b.nombre
            elif (actual == "Ubicacion"):
                b.ubicacion = linea.split(":")[1].strip()
            elif (actual == "Superficie"):
                linea = linea.split(":")[1].strip().rstrip('.')
                b.superficie = linea
            elif (actual == "Poblacion"):
                linea = linea.split(":")[1].strip().rstrip('.')
                b.poblacion = linea
            else:
                if (last == "Barrio"):
                    if (b.descripcion):
                        b.descripcion = b.descripcion + " " + linea.strip()
                    else:
                        b.descripcion = linea.strip()
                else:
                    if (b.ubicacion):
                        b.ubicacion = b.ubicacion + " " + linea.strip()
                    else:
                        b.ubicacion = linea.strip()
            if (actual != "otro"):
                last = actual
        lno += 1
    f.close()
    asoc.write(b.save(nombre) + "\n")
    asoc.close()
    os.system("chgrp www-data ../dokuwiki/data/pages/barrio/ -R; chmod g+w ../dokuwiki/data/pages/barrio -R")