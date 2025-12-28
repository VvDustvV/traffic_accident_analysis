import psycopg2
import openpyxl as opxl

import pandas as pd

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

# Funkce pro kontrolu prázdných hodnot
def null_values(table):
    counts = table.isna().sum()
    df_na_check = pd.DataFrame({
        'column': counts.index,
        'na_count': counts.values,
        'na%': (counts.values / len(table) * 100).round(2)
    })
    df_na_check = df_na_check.merge(df_column_names,
                                    left_on='column',
                                    right_on='code',
                                    how='left')
    df_na_check = df_na_check.drop(columns=['code','table_name'])
    df_na_check = df_na_check[['column','descr','name_column_en','na_count','na%']]

    row_count = pd.DataFrame({
        'column': ['TOTAL'],
        'descr': ['Celkový počet záznamů'],
        'name_column_en': ['Total row count'],
        'na_count': [len(table)],
        'na%': [' ']
    })
    df_na_check = pd.concat([df_na_check, row_count], ignore_index=True)
    return df_na_check

def get_table_column_names(table):
    column_names = table.columns
    df_column_info = pd.DataFrame({
        'column': column_names
    })
    df_column_info = df_column_info.merge(df_column_names,
                                          left_on='column',
                                          right_on='code',
                                          how='left')
    df_column_info = df_column_info.drop(columns=['code'])
    return df_column_info
