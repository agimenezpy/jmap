from psycopg2 import connect

db1 = connect("host=localhost user=gisadm password=ge0spatial dbname=digimaps")
db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur1 = db1.cursor()
cur2 = db2.cursor()

sql1 = """
select id,nombre,titulo,collect(transform(the_geom, 4326))
from callemulti
group by id,nombre,titulo
"""

sql2 = """
insert into via_transito (id, nombre, abrev, the_geom) values (%s, %s, %s, %s);
"""

cur1.execute(sql1)

try:
    print cur1.rowcount
    while True:
        row = cur1.next()
        print "Insertando %d" % row[0]
        cur2.execute(sql2, (row[0], row[1],row[2],row[3]))
except StopIteration:
    db2.commit()
except Exception, e:
    print e
    db2.rollback()


cur1.close()
db1.close()
cur2.close()
db2.close()
