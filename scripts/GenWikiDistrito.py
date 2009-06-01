#!/usr/bin/python
# -*- coding: iso8859-1 -*-
import os
from re import match, compile, findall, split, sub
from GenWiki import Barrio

class Distrito:
    def __init__(self):
        self.id = 0
        self.nombre = ""
        self.referencia = ""
        self.descripcion = ""
        self.ubicacion = ""
        self.tmpl = """
====== %(nombre)s ======

=====  Referencia =====

%(referencia)s

===== Descripción =====

%(descripcion)s

===== Ubicación =====

%(ubicacion)s

"""

    def __str__(self):
        return "Nombre: %s (%s)\nRef: %s\nDescripci\xf3n: %s\nUbicaci\xf3n: %s\n" % (self.nombre, self.id, self.referencia, self.descripcion, self.ubicacion)

    def __repr__(self):
        return self.__str__()
    
    def save(self, nombre):
        genid = self.nombre_id()
        fd = open("../dokuwiki/data/pages/distrito/%s.txt" % genid, "w")
        fd.write(self.convert(self.tmpl % self))
        fd.close()
        return "%d distrito:%s" % (self.id, genid)
    
    def __getitem__(self, strk):
        if hasattr(self, strk):
            return getattr(self, strk)
        else:
            return ""
        
    def nombre_id(self):
        clean = reduce(lambda x,y: x + " " + y, filter(lambda i: not match("^(DE|LA|LAS|DEL)$", i), sub(",|\.|'", "", self.nombre).split()))
        remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "n", "ü" : "u"}
        clean = clean.decode("latin-1").lower().encode("latin-1")
        for k, v in remp.iteritems():
            clean = clean.replace(k, v)
        end = 2
        result = ""
        while not result or registered.has_key(result):
            result = reduce(lambda x,y: x + "_" + y, clean.decode("latin-1").split()[0:end]).encode("latin-1")
            end += 1
        registered[result] = True
        return result
    
    def convert(self, strT):
        return strT.decode("latin-1").encode("UTF-8")

class Distritos:
    def __init__(self):
        self.reg = []
        self.remp = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ" : "Ñ"}
        fd = open("distritos.dat", "r")
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
            return "[[distrito:%d|%s]]" % (id, value)
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

registered = {}

if __name__ == '__main__':
    comp = compile("^[A-ZÁÉÍÓÚÑ0-9][A-ZÁÉÍÓÚÑ0-9'\.].*\((Resoluci\xf3n|Ordenanza|Decreto).*\)(\.)?$|^[A-WY-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\.].*(\.)?")
    cbarrios = compile("([^,]+,|[^,]+.$)")
    categoria = {0 : "Distrito", 1 : "otro"}
    d = Distrito()
    b = Barrio()
    distritos = Distritos()
    asoc = open("distrito_asoc.txt", "w")
    last = ""
    #3159 3181 Distritos de Asuncion BYTES 142749
    lno = 3159
    nombre = "Asuncion007-Plazas_Otros.txt"
    print "Procesando " + nombre
    f = open(nombre, 'r')
    f.seek(142749)
    links = {}
    while (lno < 3181):
        linea = f.next().strip()
        if (comp.match(linea)):
            num = 0
        else:
            num = 1
        if (isValid(linea)):
            actual = categoria.get(num)
            if (actual == "Distrito"):
                if (len(last) > 0):
                    d.descripcion = "(Articulo 4º)."
                    bars = map(lambda st: sub("\.$", "", st.replace(",", "").strip()),
                        filter(lambda x: len(x) > 0, cbarrios.split(d.ubicacion[d.ubicacion.index(":")+1:]))
                        )
                    for bar in bars:
                        if not links.has_key(bar):
                            links[bar] = b.link(bar)
                        d.ubicacion = d.ubicacion.replace(bar, links[bar])
                    asoc.write(d.save(nombre) + "\n")
                    d.__init__()
                par = linea.split("(")
                d.nombre = par[0].replace("[", "(").replace("]", ")").strip()
                d.nombre = d.nombre.replace("´", "'").replace("PARROQUIA ", "")
                if (len(par) == 2):
                    d.referencia = par[1].replace(")", "").replace(".", "")
                d.id = distritos.getId(d.nombre)
                if not d.id:
                    d.id = -1
                    print d.nombre
            else:
                if (d.ubicacion):
                    d.ubicacion = d.ubicacion + " " + linea.strip()
                else:
                    d.ubicacion = linea.strip()
            if (actual != "otro"):
                last = actual
        lno += 1
    f.close()
    d.descripcion = "(Articulo 4º)."
    bars = map(lambda st: sub("\.$", "", st.replace(",", "").strip()),
        filter(lambda x: len(x) > 0, cbarrios.split(d.ubicacion[d.ubicacion.index(":")+1:]))
        )
    for bar in bars:
        if not links.has_key(bar):
            links[bar] = b.link(bar)
        d.ubicacion = d.ubicacion.replace(bar, links[bar])
    asoc.write(d.save(nombre) + "\n")
    asoc.close()
    os.system("chgrp www-data ../dokuwiki/data/pages/distrito/ -R; chmod g+w ../dokuwiki/data/pages/distrito -R")