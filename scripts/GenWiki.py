#!/usr/bin/python
# -*- coding: iso8859-1 -*-
import os
from re import match, compile, findall, split, sub

class Calle:
    def __init__(self):
        self.id = 0
        self.nombre = ""
        self.referencia = ""
        self.descripcion = ""
        self.ubicacion = ""
        self.barrio = ""
        self.distrito = ""
        self.zonaCat = ""
        self.tmpl = """
====== %(nombre)s ======

=====  Referencia =====

%(referencia)s

===== Descripción =====

%(descripcion)s

===== Ubicación =====

%(ubicacion)s

^  Barrio  |  %(barrio)s  |
^  Distrito  |  %(distrito)s  |
^  Zona Catastral  |  %(zonaCat)s  |

"""

    def __str__(self):
        return "Nombre: %s (%s)\nRef: %s\nDescripci\xf3n: %s\nUbicaci\xf3n: %s\nBarrio: %s\nDistrito: %s\nZona Catastral: %s\n" % (self.nombre, self.id, self.referencia, self.descripcion, self.ubicacion, self.barrio, self.distrito, self.zonaCat)

    def __repr__(self):
        return self.__str__()
    
    def save(self, nombre):
        categoria = reduce(lambda x, y: x + "-" + y, split("[\-\.]", nombre.lower())[1:3])
        genid = self.nombre_id()
        fd = open("../dokuwiki/data/pages/calle/%s.txt" % genid, "w")
        fd.write(self.convert(self.tmpl % self))
        fd.close()
        return "%d calle:%s" % (self.id, genid)
    
    def __getitem__(self, strk):
        if hasattr(self, strk):
            return getattr(self, strk)
        else:
            return ""
        
    def nombre_id(self):
        clean = reduce(lambda x,y: x + " " + y, filter(lambda i: not match("^(DE|LA|LAS|DEL|Y)$", i), sub(",|\.|'|º", "", self.nombre).split()))
        remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "n", "ü" : "u"}
        clean = clean.decode("latin-1").lower().encode("latin-1")
        for k, v in remp.iteritems():
            clean = clean.replace(k, v)
        end = 2
        result = ""
        last = ""
        while not result or registered.has_key(result):
            last = result
            result = reduce(lambda x,y: x + "_" + y, clean.decode("latin-1").split()[0:end]).encode("latin-1")
            if last == result:
                result += "_" + str(self.id)
            end += 1
        registered[result] = True
        return result
    
    def convert(self, strT):
        return strT.decode("latin-1").encode("UTF-8")

class Barrio:
    def __init__(self):
        self.reg = []
        self.ref = {63:"barrio:banco_san_miguel"}
        self.remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "Ñ"}
        fd = open("barrios.dat", "r")
        try:
            while True:
                ident, nombre = fd.next().strip().split(" ", 1)
                self.reg.append((int(ident), nombre))
        except StopIteration:
            pass
        fd.close()
        
        fd = open("barrio_asoc.txt", "r")
        try:
            while True:
                ident, nombre = fd.next().strip().split(" ", 1)
                self.ref[int(ident)] = nombre
        except StopIteration:
            pass
        fd.close()

    def getId(self, nombre):
        for k, v in self.remp.iteritems():
            nombre = nombre.replace(k, v)
        nombre = nombre.upper()
        for tupla in self.reg:
            if nombre.find(tupla[1]) != -1:
                return tupla[0]
    
    def getRefId(self, id):
        return self.ref[id]
    
    def link(self, value):
        id = self.getId(value)
        if id:
            return "[[%s|%s]]" % (self.ref[id], value)
        else:
            return None

class Distrito:
    def __init__(self):
        self.reg = []
        self.ref = {13:"distrito:lambare"}
        self.remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "Ñ"}
        fd = open("distritos.dat", "r")
        try:
            while True:
                ident, nombre = fd.next().strip().split()
                self.reg.append((int(ident), nombre))
        except StopIteration:
            pass
        fd.close()
        
        fd = open("distrito_asoc.txt", "r")
        try:
            while True:
                ident, nombre = fd.next().strip().split(" ", 1)
                self.ref[int(ident)] = nombre
        except StopIteration:
            pass
        fd.close()

    def getId(self, nombre):
        for k, v in self.remp.iteritems():
            nombre = nombre.replace(k, v)
        nombre = nombre.upper()
        for tupla in self.reg:
            if nombre.find(tupla[1]) != -1:
                return tupla[0]
    
    def link(self, value):
        id = self.getId(value)
        if id:
            return "[[%s|%s]]" % (self.ref[id], value)
        else:
            print value
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

registered = {}

if __name__ == '__main__':
    src = 'TXT'
    archivos = os.listdir(src)
    archivos.sort()
    comp = [compile("^[A-ZÁÉÍÓÚÑ0-9][A-ZÁÉÍÓÚÑ0-9'\.].*\((Resoluci\xf3n|Ordenanza|Decreto).*\)(\.)?$|^[A-WY-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\.].*(\.)?"),
            compile("^Ubicaci\xf3n:.*"),
            compile("^Barrio.*:.*"),
            compile("^Distrito.*"),
            compile("^Zona.*:.*")]
    categoria = {0 : "Calle", 1 : "Ubicacion", 2 : "Barrio", 3 : "Distrito", 4 : "ZonaC", 5 : "otro"}
    c = Calle()
    barrios = Barrio()
    distritos = Distrito()
    asoc = open("asoc.txt", "w")
    last = ""
    id = 1
    for nombre in archivos:
        print "Procesando " + nombre
        f = open(src + "/" + nombre, 'r')
        try:
            while (True):
                num = 5;
                linea = f.next().rstrip("\r\n")
                for i in range(0, 5):
                    if (comp[i].match(linea)):
                        num = i
                        break
                if (isValid(linea)):
                    actual = categoria.get(num)
                    if (actual == "Calle"):
                        if (len(last) > 0):
                            asoc.write(c.save(nombre) + "\n")
                            c.__init__()
                        par = linea.split("(")
                        c.id = id
                        id += 1
                        c.nombre = par[0].replace("[", "(").replace("]", ")").strip()
                        #if match(".*([A-Z0-9ÁÉÍÓÚ]| )\.$", c.nombre):
                        #    c.nombre = c.nombre[:-1]
                        c.nombre = c.nombre.replace("´", "'")
                        c.nombre = sub("\s{2,}", " ", c.nombre)
                        if (len(par) == 2):
                            c.referencia = par[1].replace(")", "").replace(".", "")
                    elif (actual == "Ubicacion"):
                        c.ubicacion = linea.split(":")[1].strip()
                    elif (actual == "Barrio"):
                        linea = linea.split(":")[1].strip().rstrip('.')
                        c.barrio = unpack(map(barrios.link, linea.replace(" y ", ", ").split(", ")))
                        if c.barrio == None:
                            print c.id, c.nombre
                        #c.barrio = linea.replace(" y ", ", ").split(", ")
                    elif (actual == "Distrito"):
                        linea = linea.split(":")[1].strip().rstrip('.')
                        #c.distrito = linea.replace(" y ", ", ").split(", ")
                        c.distrito = unpack(map(distritos.link, linea.replace(" y ", ", ").split(", ")))
                        if not c.distrito:
                            print c.id, c.nombre
                    elif (actual == "ZonaC"):
                        c.zonaCat = unpack(map(lambda (i): i.strip(), findall("[0-9]+", linea)))
                        #for item in range(0, len(c.zonaCat)):
                        #    c.zonaCat[item] = int(c.zonaCat[item].strip())
                    else:
                        if (last == "Calle"):
                            if (c.descripcion):
                                c.descripcion = c.descripcion + " " + linea.strip()
                            else:
                                c.descripcion = linea.strip()
                        else:
                            if (c.ubicacion):
                                c.ubicacion = c.ubicacion + " " + linea.strip()
                            else:
                                c.ubicacion = linea.strip()
                    if (actual != "otro"):
                        last = actual
        except Exception, e:
            print e
        f.close()
    asoc.write(c.save(nombre) + "\n")
    asoc.close()
    os.system("chgrp www-data ../dokuwiki/data/pages/calle/ -R; chmod g+w ../dokuwiki/data/pages/calle -R")