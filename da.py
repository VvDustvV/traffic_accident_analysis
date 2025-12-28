import requests
import psycopg2
import pandas as pd
from pyproj import Transformer

def execute_sql(sql_query: str) -> list: 
    connection = None
    data = None
    try:
        connection =  psycopg2.connect(
            host='localhost',
            user='postgres',
            password='kjm57',
            dbname='postgres')
    
        cursor = connection.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        colnames = [cell[0] for cell in cursor.description]
        df_name = pd.DataFrame(data, columns=colnames)
    except Exception as E:
        print('ERROR')
    
    finally:
        if connection is not None:
            connection.close()

        return df_name


transformer = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)

def get_and_transform_data():
    query_gps = execute_sql("SELECT DISTINCT p1, p2a, p4b d, e FROM dopravni_nehody_cr.gps WHERE d < 0 LEFT JOIN dopravni_nehody_cr.nehody ON gps.p1 = nehody.p1""")
    if query_gps is not None and not query_gps.empty:
        val_e = query_gps['e'].values if (query_gps['e'].values < 0).all() else query_gps['e'].values * -1
        val_d = query_gps['d'].values if (query_gps['d'].values < 0).all() else query_gps['d'].values * -1

        lon, lat = transformer.transform(val_e, val_d)

        query_gps['lat'] = lat
        query_gps['lon'] = lon

        execute_sql("""CREATE TABLE IF NOT EXISTS opravni_nehody_cr.gps_WGS84
                          SELECT * FROM query_gps""")        
        return query_gps[['p1', 'lat', 'lon']]
    return None