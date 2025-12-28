import requests
import psycopg2
import pandas as pd
from pyproj import Transformer
from sqlalchemy import create_engine

def execute_sql(sql_query: str): 
    connection = None
    df_name = pd.DataFrame()
    try:
        connection = psycopg2.connect(
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
        print(f'ERROR: {E}')
    finally:
        if connection is not None:
            connection.close()
        return df_name

engine = create_engine('postgresql://postgres:kjm57@localhost:5432/postgres')
transformer = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)

def get_transform_and_save():
    query_str = """
        SELECT DISTINCT p1, d, e 
        FROM dopravni_nehody_cr.gps g
        WHERE d < 0
    """
    
    query_gps = execute_sql(query_str)
    
    if not query_gps.empty:
        val_e = query_gps['e'].values if (query_gps['e'].values < 0).all() else query_gps['e'].values * -1
        val_d = query_gps['d'].values if (query_gps['d'].values < 0).all() else query_gps['d'].values * -1

        lon, lat = transformer.transform(val_e, val_d)

        query_gps['lat'] = lat
        query_gps['lon'] = lon
        
        output_df = query_gps[['p1', 'lat', 'lon']]

        try:
            output_df.to_sql(
                name='gps_wgs84', 
                con=engine, 
                schema='dopravni_nehody_cr', 
                if_exists='replace', 
                index=False
            )
            print("Tabulka dopravni_nehody_cr.nehody_wgs84 byla úspěšně vytvořena.")
        except Exception as e:
            print(f"Chyba při zápisu do DB: {e}")
            
        return output_df
    
    return None


get_transform_and_save()
