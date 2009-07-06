from psycopg2 import connect
from MySQLdb import connect as connect2

db1 = connect2("localhost", "root", "myadmin", "asuncion")
db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur1 = db1.cursor()
cur2 = db2.cursor()

sql1 = """
select distinct ref_id, detalle_id from via_transito where detalle_id is not null
"""

sql2 = """
update via_transito set wiki_id = %s where id = %s;
"""

asoc = open("asoc.txt", "r")
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

cur1.execute(sql1)

try:
    print cur1.rowcount
    row = cur1.fetchone()
    while row != None:
        print "Actualizando %d" % row[0]
        cur2.execute(sql2, (wiki_links[str(row[1])], int(row[0])))
        row = cur1.fetchone()
    db2.commit()
except Exception, e:
    print "Error:", e
    db2.rollback()


cur1.close()
db1.close()
cur2.close()
db2.close()