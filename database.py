# import requests
# from requests.auth import HTTPBasicAuth 

# def get_data_from_service(service):
#     odata_username = "Jchand" 
#     odata_password = "Bakzee@123"    
#     try:
#         auth = HTTPBasicAuth(odata_username, odata_password)
#         response = requests.get(service , auth = auth)
#         response.raise_for_status()
#         service_data = response.json()

 
#         if 'd' in service_data and 'results' in service_data['d']:
#             return_data = service_data['d']['results']
#             return return_data, None
#         else:
#             return None, "No BOM data found."
#     except requests.exceptions.RequestException as e:
#         return None, str(e)

import sqlite3
import os
from Sql import set_db

def get_data_from_query(sql):
    db = 'MYdb.db'
    if not os.path.isfile(db):
        set_db()

    desc = {
        "EBELN" :"Document Number",
        "MATNR" :"Material",
        "MAKTX" :"Material Description",
        "BUKRS" :"Company code",
        "AEDAT" :"Document Creation Date",
        "BSTYP" :"Document Type",
        "MTART" :"Material Type",
        "ERSDA" :"Material Creation Date",
    }
    try:
       conn = sqlite3.connect(db)
       cur = conn.cursor()
       cur.execute(sql)
       rows = cur.fetchall()
    except Exception as e:
           print(str(e))
    column_names = []
    for description in cur.description:
        if desc.get(description[0]):
            column_names.append(desc.get(description[0]))
        else:
            column_names.append("Total Number of orders")
    conn.commit()
    conn.close()
    return  column_names , rows