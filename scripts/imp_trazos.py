from psycopg2 import connect

db1 = connect("host=192.168.0.2 user=gisadm password=ge0spatial dbname=asuncion")
db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur1 = db1.cursor()
cur2 = db2.cursor()

sql1 = """
select id,tipo,prioridad,zorder,
case
when c1.id > 0 then (select direccion from callemulti c2 where c2.id = c1.id limit 1) 
else 0
end as direccion,
transform(the_geom, 4326)
from calle c1
where the_geom is not null
order by gid
"""

sql2a = """
insert into via_trazo(ref_id,tipo_id,prioridad,zorder,num_ini,num_fin,direccion,the_geom) values (%s, %s, %s, %s, 0,0, %s, %s);
"""

sql2b = """
insert into via_trazo(tipo_id,prioridad,zorder,num_ini,num_fin,direccion,the_geom) values (%s, %s, %s, 0,0, %s, %s);
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
        print "Insertando %d" % cur1.rownumber
        if row[0] > 0:
            cur2.execute(sql2a, (row[0],tipo_vias[row[1]],row[2],row[3],row[4],row[5]))
        else:
            cur2.execute(sql2b, (tipo_vias[row[1]],row[2],row[3],row[4],row[5]))
except StopIteration:
    db2.commit()
except Exception, e:
    print e
    db2.rollback()


cur1.close()
db1.close()
cur2.close()
db2.close()