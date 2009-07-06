#!/usr/bin/python
# -*- coding: iso8859-1 -*-
import os
from re import match, compile, findall, split, sub
from GenWiki import Barrio

class Plaza:
    def __init__(self):
        self.id = 0
        self.nombre = ""
        self.referencia = ""
        self.descripcion = ""
        self.ubicacion = ""
        self.barrio = ""
        self.ctacte = ""
        self.tmpl = """
====== %(nombre)s ======

=====  Referencia =====

%(referencia)s

===== Descripción =====

%(descripcion)s

===== Cta. Cte. Ctral =====

%(ctacte)s

===== Ubicación =====

%(ubicacion)s

^  Barrio  |  %(barrio)s  |

"""

    def __str__(self):
        return "Nombre: %s (%s)\nRef: %s\nDescripci\xf3n: %s\nCta. Cte. Ctral: %s\nUbicaci\xf3n: %s\nBarrio: %s\n" % (self.nombre, self.id, self.referencia, self.descripcion, self.ctacte, self.ubicacion, self.barrio)

    def __repr__(self):
        return self.__str__()
    
    def save(self, nombre):
        genid = self.nombre_id()
        fd = open("../dokuwiki/data/pages/plaza/%s.txt" % genid, "w")
        fd.write(self.convert(self.tmpl % self))
        fd.close()
        return "%d plaza:%s" % (self.id, genid)
    
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
            if end > len(clean):
                result += "_" + str(self.id)
            end += 1
        registered[result] = True
        return result
    
    def convert(self, strT):
        return strT.decode("latin-1").encode("UTF-8")

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
    comp = [compile("^[A-ZÁÉÍÓÚÑ0-9][A-ZÁÉÍÓÚÑ0-9'\.].*\((Resoluci\xf3n|Ordenanza|Decreto).*\)(\.)?$|^[A-WY-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\.].*(\.)?"),
                    compile("^Ubicaci\xf3n:.*"),
                    compile("^Cta\. Cte\. Ctral:.*"),
                    compile("^Barrio.*:.*")]
    p = Plaza()
    barrios = Barrio()
    categoria = {0 : "Plaza", 1 : "Ubicacion", 2 : "Cta. Cte. Ctral", 3 : "Barrio", 4 : "otro"}
    asoc = open("plaza_asoc.txt", "w")
    dat = open("plaza.dat", "w")
    last = ""
    #2 1447 Plazas de Asuncion BYTES 51596
    lno = 1
    nombre = "Asuncion007-Plazas_Otros.txt"
    print "Procesando " + nombre
    f = open(nombre, 'r')
    f.seek(43)
    links = {}
    id = 1
    while (lno < 1448):
        num = 4
        linea = f.next().strip()
        for i in range(0, 4):
            if (comp[i].match(linea)):
                num = i
                break
        if (isValid(linea)):
            actual = categoria.get(num)
            if (actual == "Plaza"):
                if (len(last) > 0):
                    asoc.write(p.save(nombre) + "\n")
                    p.__init__()
                par = linea.split("(")
                p.id = id
                p.nombre = par[0].replace("[", "(").replace("]", ")").strip()
                p.nombre = p.nombre.replace("´", "'")
                p.nombre = sub("\s{2,}", " ", p.nombre)
                dat.write("%d\t%s\n" % (p.id, p.nombre))
                if (len(par) == 2):
                    p.referencia = par[1].replace(")", "").replace(".", "")
                id += 1
            elif (actual == "Ubicacion"):
                p.ubicacion = linea.split(":")[1].strip()
            elif (actual == "Cta. Cte. Ctral"):
                p.ctacte = linea.split(":")[1].strip()
            elif (actual == "Barrio"):
                linea = linea.split(":")[1].strip().rstrip('.')
                p.barrio = unpack(map(barrios.link, linea.replace(" y ", ", ").split(", ")))
                if p.barrio == None:
                    print p.id, p.nombre
            else:
                if (last == "Plaza"):
                    if (p.descripcion):
                        p.descripcion = p.descripcion + " " + linea.strip()
                    else:
                        p.descripcion = linea.strip()
                else:
                    if (p.ubicacion):
                        p.ubicacion = p.ubicacion + " " + linea.strip()
                    else:
                        p.ubicacion = linea.strip()
            if (actual != "otro"):
                last = actual
        lno += 1
    f.close()
    asoc.write(p.save(nombre) + "\n")
    asoc.close()
    dat.close()
    os.system("chgrp www-data ../dokuwiki/data/pages/plaza/ -R; chmod g+w ../dokuwiki/data/pages/plaza -R")