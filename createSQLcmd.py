#!/usr/bin/env python3
import logging
import sys
from pprint import pformat
import psycopg2
import ComplexFunctionForColumn

log = logging.getLogger(__name__)

DB_HOST = "192.168.50.213"
DB_PORT = 5432
DB_NAME = ""
DB_USER = ""   # change if your user is different
DB_PASSWORD = ""

NULL_STR = 'NULL'
def db_value(recVAL):
    if recVAL == NULL_STR: return 'NULL'
    if isinstance(recVAL, str): return f"'{recVAL}'"
    return recVAL


QUERY_MODULE = '''SELECT module_name FROM public.module_info
WHERE geometry IS NULL
ORDER BY module_no ASC
'''
geo_str = { 'F': 'Full', 'T': 'Top', 'B': 'Bottom', 'L': 'Left', 'R': 'Right', '5': 'Five', }
def get_geo(moduleID):
    '320MHL1WCNT0152'
    identifier = moduleID[5]
    log.debug(f'[GotIdentifier] char "{identifier}" for moduleID {moduleID}')
    return db_value(geo_str.get(identifier, "NULL"))

res_str = { 'H': 'HD', 'L': 'LD' }
def get_res(moduleID):
    '320MHL1WCNT0152'
    identifier = moduleID[4]
    log.debug(f'[GotIdentifier] char "{identifier}" for moduleID {moduleID}')
    return db_value(res_str.get(identifier, "NULL"))


bp_material_dict = {'W': 'CuW', 'P': 'PCB', 'T': 'Titanium', 'C': 'Carbon fiber'}
def get_bpmaterial(moduleID):
    '320MHL1WCNT0152'
    identifier = moduleID[7]
    log.debug(f'[GotIdentifier] char "{identifier}" for moduleID {moduleID}')
    return db_value(bp_material_dict.get(identifier, "NULL"))

roc_version_dict = {'X': 'Preseries', '2': 'HGCROCV3b-2', '4': 'HGCROCV3b-4', 'B': 'HGCROCV3b-3' ,'C': 'HGCROCV3c', 'D': 'HGCROCV3d', 'E': 'HGCROCV3e', 'F': 'HGCROCV3f'}
def get_rocv(moduleID):
    '320MHL1WCNT0152'
    identifier = moduleID[8]
    log.debug(f'[GotIdentifier] char "{identifier}" for moduleID {moduleID}')
    return db_value(roc_version_dict.get(identifier, "NULL"))


    #thicknessTYPE = { '1':'300um', '2':'200um', '3':'120um', '4':'300um partial','5':'200um partial', '6':'120um partial' }
#senthic_str = { '1':300, '2':200, '3':120, '4':300, '5':200, '6':120 } ### output is a "real" ### this is only for sensor
senthic_str = { '1':120, '2':200, '3': 300 } ### output is a "real" ### this is for silicon module
def get_senthick(moduleID):
    '320MHL1WCNT0152'
    identifier = moduleID[6]
    log.debug(f'[GotIdentifier] char "{identifier}" for moduleID {moduleID}')
    return db_value(senthic_str.get(identifier, "NULL"))



def selected_moduleID(sqlQUERYstr) -> list:
    module_list = []
    try:
        # connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = conn.cursor()

        # execute query
        cursor.execute(sqlQUERYstr)

        # fetch results
        rows = cursor.fetchall()

        # store module_name into list
        module_list = [row[0] for row in rows]

        log.debug(f'[Get ModuleID list] {module_list}')

    except Exception as e:
        print("Database error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    return module_list
def insert_info(sqlQUERYstr) -> list:
    result = ''
    try:
        # connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = conn.cursor()

        # execute query
        cursor.execute(sqlQUERYstr)

        # fetch results
        #result = cursor.fetchall()

        # store module_name into list

        #log.debug(f'[result] {result}')

    except Exception as e:
        print("Database error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    return result


if __name__ == '__main__':
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
                        format=f'%(levelname)-7s%(filename)s#%(lineno)s %(funcName)s() >>> %(message)s',
                        datefmt='%H:%M:%S')

    

    
   #SQLfile_search_moduleID = 'task1.search_null_geometry.sql'
   #sqlfile_evaluate_cmd = 'task1.evaluate_geometry.sql'
    SQLfile_search_moduleID = sys.argv[1]
    sqlfile_evaluate_cmd = sys.argv[2]


    sqlcmd_search_moduleID = open(SQLfile_search_moduleID, 'r').read()
    log.debug(f'[LoadSQLCMD] Search ModuleID command: \n{sqlcmd_search_moduleID}\n')
    moduleIDs = selected_moduleID(sqlcmd_search_moduleID)
    log.debug(f'[ModuleID list] Selected ModuleIDs: {moduleIDs}')
    

    sqlcmd_evaluate_cmd = open(sqlfile_evaluate_cmd, 'r').read().strip()
    sqlcmd_evaluate_cmd = "f'''" + sqlcmd_evaluate_cmd + "'''"

    log.debug(f'[LoadSQLCMD] evaluate SQL cmd \n{sqlcmd_evaluate_cmd}\n')
    generated_sqlcmd = eval(sqlcmd_evaluate_cmd, locals(), vars(ComplexFunctionForColumn))
    
    print(generated_sqlcmd)
    #insert_info(generated_sqlcmd)


