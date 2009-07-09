from psycopg2 import connect

db1 = connect("host=192.168.0.2 user=gisadm password=ge0spatial dbname=asuncion")
db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur1 = db1.cursor()
cur2 = db2.cursor()

sql1 = """
select id,ref,nombre,tipo_id,parent_id,zorder,transform(the_geom, 4326)
from limite_politico order by id
"""

sql2 = """
insert into limite_politico (ref,nombre,tipo_id,parent_id,zorder,the_geom) values (%s,%s,%s,%s,%s,%s)
"""

cur1.execute(sql1)

try:
    print cur1.rowcount
    while True:
        row = cur1.next()
        print "Insertando %d" % row[0]
        cur2.execute(sql2, (row[1],row[2],row[3],row[4],row[5],row[6]))
except StopIteration:
    db2.commit()
except Exception, e:
    print e
    db2.rollback()


cur1.close()
db1.close()
cur2.close()
db2.close()
