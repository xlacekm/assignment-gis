import cherrypy
import psycopg2
import json
import os, os.path

conn_string = "dbname='gisp' user='postgres'"
try:
    #print "Connecting to database\n"
    conn = psycopg2.connect(conn_string)
    #print "done"
    cursor = conn.cursor()
except:
    print "Unable to connect"

lng = 18.098340299765397
lat = 48.51165243528095

class web(object):
    @cherrypy.expose
    def index(self):
            return open('index.html')

    @cherrypy.expose
    def clear(self):
        print 'cistim'

    @cherrypy.expose
    #Najblizsia cesta
    def Nearest(self,lng,lat,distance):
        cursor.execute("""  SELECT ST_AsGeoJSON(ST_Transform(way,4326)) as data,ST_distance(ST_Transform(way,4326),ST_SetSRID(ST_Point(%f,%f),4326)) distance
            from planet_osm_line
            where (route='bicycle' or bicycle='yes')
            and ST_Intersects(
              ST_Transform(way,4326),
              ST_Buffer(ST_SetSRID(ST_Point(%f,%f),4326),
              %f))
             ORDER BY distance
             limit 1;
             """ %(float(lng),float(lat),float(lng),float(lat),float(distance)))

        respond = []
        for record in cursor:
            respond.append({'type':'Feature','geometry':json.loads(record[0]),'properties':{}})
        response = {'type':'FeatureCollection','features':respond}


        return json.dumps(response)

    @cherrypy.expose
    #Okolie
    def Surroundings(self,lng,lat,distance):
        cursor.execute(""" SELECT ST_AsGeoJSON(ST_Transform(way,4326)) as data
            from planet_osm_line
            where (route='bicycle' or bicycle='yes')
            and ST_Intersects(
              ST_Transform(way,4326),
              ST_Buffer(ST_SetSRID(ST_Point(%f,%f),4326),
              %f));
             """ %(float(lng),float(lat),float(distance)))

        respond = []
        for record in cursor:
            respond.append({'type':'Feature','geometry':json.loads(record[0]),'properties':{}})
        response = {'type':'FeatureCollection','features':respond}


        return json.dumps(response)

    @cherrypy.expose
    #Lekaren pri ceste
    def Pharmacy(self,lng,lat,distance):
        cursor.execute("""with cesta as (
                                SELECT ST_Transform(way,4326) as way,ST_distance(ST_Transform(way,4326),ST_SetSRID(ST_Point(%f,%f),4326)) distance
                                from planet_osm_line
                                where (route='bicycle' or bicycle='yes')
                                and ST_Intersects(
                                  ST_Transform(way,4326),
                                  ST_Buffer(ST_SetSRID(ST_Point(%f,%f),4326),
                                  0.5))
                                 ORDER BY distance
                                 limit 1
                                    )
                                SELECT ST_AsGeoJSON(ST_Transform(p.way,4326))    from cesta
                                                                                join planet_osm_point p
                                                                                on ST_Dwithin(ST_Transform(p.way,4326),ST_Transform(cesta.way,4326),%f)
                                                                                WHERE amenity = 'pharmacy'
                 """ %(float(lng),float(lat),float(lng),float(lat),float(distance)))

        respond = []
        for record in cursor:
            respond.append({'type':'Feature','geometry':json.loads(record[0]),'properties':{}})
        response = {'type':'FeatureCollection','features':respond}


        return json.dumps(response)

    @cherrypy.expose
    #Jedlo v okoli
    def Food(self,lng,lat,distance):
        cursor.execute("""SELECT ST_AsGeoJSON(ST_Transform(way,4326)) as data
            from planet_osm_point
            where (amenity = 'pub' or amenity = 'restaurant')
            and ST_Dwithin(
              ST_Transform(way,4326),
              ST_SetSRID(ST_Point(%f,%f),4326),%f);
             """ %(float(lng),float(lat),float(distance)))

        respond = []
        for record in cursor:
            respond.append({'type':'Feature','geometry':json.loads(record[0]),'properties':{}})
        response = {'type':'FeatureCollection','features':respond}


        return json.dumps(response)





if __name__ == "__main__":
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/generator': {
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }

     }
webapp = web()
cherrypy.quickstart(webapp, '/', conf)