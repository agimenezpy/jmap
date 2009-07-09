from psycopg2 import connect

db1 = connect("host=192.168.0.2 user=gisadm password=ge0spatial dbname=asuncion")
db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur1 = db1.cursor()
cur2 = db2.cursor()

sql1 = """
select id,nombre,titulo,tipo,zorder,prioridad,collect(transform(the_geom, 4326))
from callemulti
group by id,nombre,titulo,tipo,zorder,prioridad
"""

sql2 = """
insert into via_transito (id, nombre, abrev, tipo_id, zorder, prioridad, the_geom) values (%s, %s, %s, %s, %s, %s, %s);
"""

sql2c = "select id, regexp_replace(descripcion, 'ria', 'rio') from tipo_via"

cur2.execute(sql2c)
tipo_vias = {}
try:
    while True:
        row = cur2.next()
        tipo_vias[row[1]] = row[0]
except StopIteration:
    pass
except Exception, e:
    print e

tipo_vias['footway'] = tipo_vias['peatonal']
tipo_vias['pedestrian'] = tipo_vias['pasaje']

cur1.execute(sql1)

try:
    print cur1.rowcount
    while True:
        row = cur1.next()
        print "Insertando %d" % row[0]
        cur2.execute(sql2, (row[0], row[1],row[2],tipo_vias[row[3]],row[4],row[5],row[6]))
except StopIteration:
    db2.commit()
except Exception, e:
    print e
    db2.rollback()


cur1.close()
db1.close()
cur2.close()
db2.close()
