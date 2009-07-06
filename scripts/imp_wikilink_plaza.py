from psycopg2 import connect

db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur2 = db2.cursor()

sql1 = """
select id from area_interes where tipo_id = '2' and to_tsvector('spanish', nombre) @@ to_tsquery('%s')
"""

sql2 = """
update area_interes set wiki_id = %s where id = %s;
"""

asoc = open("plaza_asoc.txt", "r")
wiki_links = {}
try:
    while True:
        id, wikilink = asoc.next().strip().split()
        wiki_links[id] = wikilink
except StopIteration:
    pass
except Exception, e:
    print e
asoc.close()

plaza = open("plaza.dat", "r")

try:
    while True:
        id, nombre = plaza.next().split("\t", 1)
        nombre = nombre.strip().replace(" ", " & ").replace("'",r"\'")
        cur2.execute(sql1 % nombre)
        print nombre, cur2.rowcount
        if cur2.rowcount == 1:
            row = cur2.fetchone()
            if row != None:
                print "Actualizando %s" % row[0]
                cur2.execute(sql2,  (wiki_links[id], int(row[0])))
        elif cur2.rowcount > 1:
            print cur2.fetchall(), nombre
except StopIteration:
    db2.commit()
except Exception, e:
    print "Error:", e
db2.rollback()
plaza.close()

cur2.close()
db2.close()