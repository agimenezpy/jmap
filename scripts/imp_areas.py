from psycopg2 import connect

db1 = connect("host=192.168.0.2 user=gisadm password=ge0spatial dbname=asuncion")
db2 = connect("host=localhost user=gisadm password=ge0spatial dbname=guiadigital")

cur1 = db1.cursor()
cur2 = db2.cursor()

# plaza = xpath_string(attrs, '/attrs/landuse') = 'recreation_ground' and (name ~* 'plaza' or name ~* 'plazoleta')
# parque = xpath_string(attrs, '/attrs/leisure') = 'park'
# deporte = xpath_string(attrs, '/attrs/leisure') = 'sports_centre'
# comercio = xpath_string(attrs, '/attrs/landuse') = 'retail'
# universidad = xpath_string(attrs, '/attrs/amenity') = 'university'
# estadio = xpath_string(attrs, '/attrs/leisure') = 'stadium'
# comercial = xpath_string(attrs, '/attrs/landuse') = 'commercial'
# hospital = xpath_string(attrs, '/attrs/amenity') = 'hospital'
# terminal = xpath_string(attrs, '/attrs/building') = 'station'
# edificio = xpath_string(attrs, '/attrs/building') = 'yes'
# hipodromo = xpath_string(attrs, '/attrs/landuse') = 'recreation_ground' and not (name ~* 'plaza' or name ~* 'plazoleta')
# cementerio = xpath_string(attrs, '/attrs/landuse') = 'cemetery'
# estacion = xpath_string(attrs, '/attrs/railway') = 'station'
sql1 = """
select fid,name,z_order,transform(the_geom, 4326)
from area_interes_old
where xpath_string(attrs, '/attrs/railway') = 'station'
"""

sql2a = """
insert into area_interes (nombre,zorder,tipo_id,the_geom) values (%s,%s,%s,%s)
"""

sql2b = """
select id from tipo_area_interes where descripcion = 'estacion';
"""

cur1.execute(sql1)
cur2.execute(sql2b)
tipo = cur2.fetchone()[0]

try:
    print cur1.rowcount
    while True:
        row = cur1.next()
        print "Insertando %d: %s" % (row[0], row[1])
        cur2.execute(sql2a, (row[1],row[2],tipo,row[3]))
except StopIteration:
    db2.commit()
except Exception, e:
    print e
    db2.rollback()


cur1.close()
db1.close()
cur2.close()
db2.close()
