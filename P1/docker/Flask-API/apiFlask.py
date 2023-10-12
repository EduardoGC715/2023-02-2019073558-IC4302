import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("bibliotec-98a06-firebase-adminsdk-qiahh-ea76f83463.json")
firebase_admin.initialize_app(cred)
import datetime as dt
import bson
from flask import Flask, request, render_template_string, current_app, g, jsonify
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from flask_cors import CORS
from os import environ
import logging
from prometheus_client import start_http_server, Counter, Gauge
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import oci
import logging
from borneo.iam import SignatureProvider
from borneo import (Regions, NoSQLHandle, NoSQLHandleConfig, PutRequest)
import time
import json
import random
import requests
import oracledb

# Código basado de
# https://docs.oracle.com/en-us/iaas/tools/python/2.112.0/api/object_storage/client/oci.object_storage.ObjectStorageClient.html
# https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.112.0/objectstorage/get_object.py.html
# https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.112.0/objectstorage/list_objects.py.html
# https://apexapps.oracle.com/pls/apex/r/dbpm/livelabs/run-workshop?p210_wid=642

config = {
   "key_content": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDM7xOlheMG9Jvn
DUOry1A+XuB6zuCi5nRSiGOqmbQfR/2/20wKteKTbIfRVe6MGGdHdpFTM1ZFZCPd
Vpru6KBk6Aona+iQWXK7tMKfhNjOTkpj88oeFBPx07mELTQLednaZDaojUhPmWZ6
/tE0BgzAVeu4nyu0KyxmFAL8x2ncXi/BFJgEsRaU0OkUns/VfUtFEUWD8BIzlPbR
L/Gi36ZxhqkMPpMs6FwUikYT1eU9KJ4oFgnxX3D4Vi9Fzcg0wrgRFYnNfEOGJZYE
rOLnrqFeowARYAH+nzowjkQ6CSb1QadGq7hzjismxQmxRs56SASKYkrVYVCSBG37
BMwfYDjrAgMBAAECggEAA8NIBbwFmnUXVRC7SLDnp52FBaboHQBE69cGmB/7sgSt
C2lyu1JHohQAvRPqLgxXU8qWNIQ2y04MEoj/40Rw3X7H4PLBnGo9XxDx7zfjOzaD
ddOzcbCbWnoGvVSPJhQgrzqJKQ3JtsccSJnb1tay7pJ6ojMvUZQ8BnZ2ROnsbwK1
62uoZG7XmHaqQJY7z2JZ1a/6Tt6YP2ufaAZxs8tqbfqKM369LIL/QKJNxkEsAncN
/eAiKjyhgPMPfOLxGnS/dWZgPdNjy92+Nw9iYs+5NVqRGiJpiGf4ovWNNPiIG3oL
KbVDhXt3ynwqIS6g6j5ILWicpiUmtstKOeU4oMIOAQKBgQD/sDU/BZ7ljjTQpb/p
YJvRGITpHcXovyH5z/GK6s3gCaJq9/tUihXzaZH5s1V5UOUFVb923KYbUKalyGlF
GRusMF5GWiI55cqFXI3R9KFlu4UJAglXuCxsWHejweRBV2a4DiVOlj45WuyLeJLR
jsL4CvflVMTZsgVIrObB/Ti9awKBgQDNLweqq44ksVDGMKWEZIlIz0PjPUSWhIDa
eUMjuazjLxiJ8yiUmf4AE7vK6SoiP9uudx2xWnnZyVIe/PJXseFbINuBh0k9jU6R
H8SOSLFS85TcrCl+ImNDygHiczxaVuiykjYpLIaPqT/BTayXnGiX+xBSwweA9Ng1
pZni2fXSgQKBgGfMM8Fy2a+dDEnLj94BDyBSUNqF8KrstLFCPm9DpPIXVy0PoKMQ
L5sSN2Vj7QYD1gVVaxWou3IJSq2wbzPS3o4HUK5EtvJEG/QJv7UFF2RCPN6MShin
NrmBLIh5FN2FyrhbXb/KdFY6WB7Cgu+5geLKKRqbUBKEF2sKbd9AmgEjAoGATg93
ZjnwUQtYhJ4bSlwJUrbvx/MWNgFhGD0MCvpnyOKw/kKRDL/tP1BCoLbGPdN3m09b
745RT0blRD7NYAmfh9DfUc8LUSyCWHnyiIMlWz6qQq4I9yDUDQU8ZE+dBW2NB+rS
SiXTZ7JnO/52DBQIQtHUavgh0bDU1MwU2JY9jIECgYEA4GumexTeBxhwomIKd4bn
5wbYGAgdg6TPym7mGHpEVwVc/SYg1mTeOp988ZIbzdLcjQLY9E5Kpd/dZzVZ5izs
IzI5Mtbaa6QFL3QyhFnyiANbyfuw4rJTGdkUgKlP/jsabVVfMw2x+w5lwPI8oU5E
wf4QTCyd9noRs4piFx6/9A0=
-----END PRIVATE KEY-----""",
  "user": "ocid1.user.oc1..aaaaaaaaxmr6fc3rqsoest3yfqamz3yjrulxovyua2xuwibxb6bdjlyj6lmq",
  "fingerprint": "aa:4e:83:38:68:4d:38:90:7c:14:b7:84:64:f6:c3:e1",
  "tenancy": "ocid1.tenancy.oc1..aaaaaaaab2j6gk2b33sutg2bhoga5zekg3j5su23tygzw6nw5es4jxdts4ya",
  "region": "us-chicago-1"
 }


oci.config.validate_config(config)
object_storage = oci.object_storage.ObjectStorageClient(config)
compartment_id = config['tenancy']
namespace = object_storage.get_namespace().data
bucket_name = "bibliotec"

at_provider = SignatureProvider(tenant_id=config["tenancy"],
                                user_id=config["user"],
                                private_key=config["key_content"], 
                                fingerprint=config["fingerprint"])

region = Regions.US_CHICAGO_1

config2 = NoSQLHandleConfig(region, at_provider)

handle = NoSQLHandle(config2)

def get_db():
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db

# Método para escribir en la base de datos NoSQL en Oracle Cloud
def write_a_record(handle, table_name, record):
    request = PutRequest().set_table_name(table_name)
    request.set_value(record)
    handle.put(request)
    return
db = LocalProxy(get_db)

# Codigo basado en https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
# https://github.com/prometheus/client_python

# Create a metric to track time spent and requests made.
REQUEST_COUNT = Counter('flask_http_requests', 'Number of HTTP requests received')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 
app = Flask(__name__)


# metricas de cada endpoint para prometheus
metrics = {
    'get_pages': {
        'REQUEST_COUNT': Counter('flask_http_requests_autonomous', 'Number of HTTP requests received'),
        'MAX_TIME': Gauge('request_processing_seconds_max_autonomous', 'Maximum request processing time in autonomous endpoint'),
        'MIN_TIME': Gauge('request_processing_seconds_min_autonomous', 'Minimum request processing time in autonomous endpoint'),
        'AVG_TIME': Gauge('request_processing_seconds_avg_autonomous', 'Average request processing time in autonomous endpoint')
    },
    'get_data': {
        'REQUEST_COUNT': Counter('flask_http_requests_mongo', 'Number of HTTP requests received in mongo endpoint'),
        'MAX_TIME': Gauge('request_processing_seconds_max_mongo', 'Maximum request processing time in mongo endpoint'),
        'MIN_TIME': Gauge('request_processing_seconds_min_mongo', 'Minimum request processing time in mongo endpoint'),
        'AVG_TIME': Gauge('request_processing_seconds_avg_mongo', 'Average request processing time in mongo endpoint')
    },
    'login': {
        'REQUEST_COUNT': Counter('flask_http_requests_login', 'Number of HTTP requests received in login endpoint'),
        'MAX_TIME': Gauge('request_processing_seconds_max_login', 'Maximum request processing time in login endpoint'),
        'MIN_TIME': Gauge('request_processing_seconds_min_login', 'Minimum request processing time in login endpoint'),
        'AVG_TIME': Gauge('request_processing_seconds_avg_login', 'Average request processing time in login endpoint')
    },
    'register': {
        'REQUEST_COUNT': Counter('flask_http_requests_register', 'Number of HTTP requests received in register enpoint'),
        'MAX_TIME': Gauge('request_processing_seconds_max_register', 'Maximum request processing time in register endpoint'),
        'MIN_TIME': Gauge('request_processing_seconds_min_register', 'Minimum request processing time in register endpoint'),
        'AVG_TIME': Gauge('request_processing_seconds_avg_register', 'Average request processing time in register endpoint')
    }
}

# diccionarios que almacenan los tiempos maximos minimos promedio u numero de requests por endpoint
times_max = {}
times_min = {}
times_avg = {}
times_count = {}

# contador de tiempo por request hecho utilizando https://sureshdsk.dev/flask-decorator-to-measure-time-taken-for-a-request
@app.before_request
def logging_before():
    # Store the start time for the request
    g.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    global times_max, times_min, times_avg, times_count
    logger.debug(f"Endpoint: {request.endpoint}")
    endpoint = request.endpoint
    total_time = time.perf_counter() - g.start_time
    time_in_ms = int(total_time)
    
    # Initialize metrics for the endpoint if it's the first time
    if endpoint not in times_count:
        times_count[endpoint] = 0
        times_max[endpoint] = 0
        times_min[endpoint] = float('inf')
        times_avg[endpoint] = 0
    
    times_count[endpoint] += 1

    times_max[endpoint] = max(times_max[endpoint], time_in_ms)
    times_min[endpoint] = min(times_min[endpoint], time_in_ms)
    times_avg[endpoint] += time_in_ms

    if endpoint in metrics:
        metrics[endpoint]['MAX_TIME'].set(times_max[endpoint])
        metrics[endpoint]['MIN_TIME'].set(times_min[endpoint])
        metrics[endpoint]['REQUEST_COUNT'].inc()
        avg_value = times_avg[endpoint]
        if times_count[endpoint] != 0:
            avg_value = avg_value / times_count[endpoint]
            
        metrics[endpoint]['AVG_TIME'].set(avg_value)
    return response

# enable cors
CORS(app)

# AUTONOMOUS CONNECTION
def connectAutonomousDB():
    try:
        
        cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-chicago-1.oraclecloud.com))(connect_data=(service_name=gcea482f4f1b83b_ic4302_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
        connection=oracledb.connect(
            user="ADMIN",
            password="thisiswrongNereo08",
            dsn=cs)
        
        return connection
    except Exception as e:
        # Handle the exception
        logger.debug(f"Error connecting to AutonomousDB: {e}")
        return None
    
def read_lob(lob):
    """Utility function to read LOB content."""
    if hasattr(lob, "read"):
        content = lob.read()
        # Check if the content is bytes and decode if needed
        if isinstance(content, bytes):
            return content.decode('utf-8')
        return content
    return lob

def createAutonomousView(search_term):
    cur = autonomous.cursor()
    
    try:
        cur.execute('DROP MATERIALIZED VIEW SearchView')
    except:
        pass
    
    params = [search_term]
    
    # Call the procedure using the list of parameters, facet0 ,facet1, facet2, facet3, facet4, facet5, facet6, facet7, facet8, facet9
    cur.callproc('createSearchView', params)
 
    
def searchAutonomousFacets():
    cur = autonomous.cursor()

    out_val = cur.var(oracledb.DB_TYPE_CURSOR) 

    params = [out_val]

    # Call the procedure using the list of parameters
    cur.callproc('search_facets', params)

    # Get the returned SYS_REFCURSOR from the out_val and fetch the results
    result_cursor = out_val.getvalue()
    rows = result_cursor.fetchall()

    # Don't forget to close the result_cursor when done
    result_cursor.close()
    
    pages = []
    for row in rows:
        # Prepare the page dictionary
        page = {
            'facetType': row[0],
            'facetValue': row[1],
            'facetCount': row[2]}
        pages.append(page)
    
    cur.close()
    return pages


def searchAutonomous():
    cur = autonomous.cursor()
    
    cur.execute('SELECT * FROM SearchView')
    result = cur.fetchall()
    
    pages = []
    for row in result:
        # Prepare the page dictionary
        page = {
            'pageId': row[0],
            'pageTitle': row[1],
            'pageNamespace': row[2],
            'pageRedirect': row[3],
            'pageHasRedirect': row[4],
            'pageRestrictions': row[5],
            'siteInfoName': row[6],
            'siteInfoDBName': row[7],
            'siteLanguage': row[8],
            'pageLastModified': row[9].isoformat() if isinstance(row[9], dt.datetime) else row[9],
            'pageLastModifiedUser': row[10],
            'pageBytes': row[11],
            'pageText': read_lob(row[12]),
            'pageWikipediaLink': row[13],
            'pageWikipediaGenerated': row[14],
            'pageLinks': row[15],
            'pageNumberLinks': row[16],
            'pagePoints': row[17]}
        pages.append(page)
    
    cur.close()
    
    facets = []
    
    facets = searchAutonomousFacets()
    
    result = {
        "docs": pages, 
        "facets": facets}
    
    return result

def searchAutonomousWithFacets( facet0 ,facet1, facet2, facet3, facet4, facet5, facet6, facet7, facet8, facet9):
    cur = autonomous.cursor()
    
    out_val = cur.var(oracledb.DB_TYPE_CURSOR) 

    params = [facet0 ,facet1, facet2, facet3, facet4, facet5, facet6, facet7, facet8, facet9, out_val]

    # Call the procedure using the list of parameters
    cur.callproc('search_facets', params)

    # Get the returned SYS_REFCURSOR from the out_val and fetch the results
    result_cursor = out_val.getvalue()
    rows = result_cursor.fetchall()

    # Don't forget to close the result_cursor when done
    result_cursor.close()
    
    pages = []
    for row in rows:
        # Prepare the page dictionary
        page = {
            'pageId': row[0],
            'pageTitle': row[1],
            'pageNamespace': row[2],
            'pageRedirect': row[3],
            'pageHasRedirect': row[4],
            'pageRestrictions': row[5],
            'siteInfoName': row[6],
            'siteInfoDBName': row[7],
            'siteLanguage': row[8],
            'pageLastModified': row[9].isoformat() if isinstance(row[9], dt.datetime) else row[9],
            'pageLastModifiedUser': row[10],
            'pageBytes': row[11],
            'pageText': read_lob(row[12]),
            'pageWikipediaLink': row[13],
            'pageWikipediaGenerated': row[14],
            'pageLinks': row[15],
            'pageNumberLinks': row[16],
            'pagePoints': row[17]}
        pages.append(page)
        
    cur.close()
    return pages

def getAutonomousPoints(pageId):
    cur = autonomous.cursor()
    cur.execute("select PAGEPOINTS from PAGES where pageid = " + pageId)
    
    row = cur.fetchone()
    cur.close()
    return row[0] if row else None

# MONGO CONNECTION
def mongoDBConnection (): 
    try:
        app.config["MONGO_URI"] = "mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/bibliotec"
        mongo = PyMongo(app)
        return mongo
    except Exception as e:
        logger.debug(f"An error occurred: {e}")


#MONGO OPERATIONS

def isValidDate(dateStr):
    try:
        dt.datetime.strptime(dateStr, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def textSearchQuery(searchQuery):
    pipeline = [
    {
        '$search': {
            'index': 'mainIndex', 
            'facet': {
                'operator': {
                    "compound": {
                        "should": [
                            {
                                "text":{
                                    "path":{
                                        "wildcard": "*"
                                    },
                                    "query": str(searchQuery)
                                }
                            },
                        ],
                        "filter":[],
                        "minimumShouldMatch": 1
                    }
                }, 
                'facets': {
                    'PageLastModifiedUserFacet': {
                        'type': 'string', 
                        'path': 'PageLastModifiedUser'
                    }, 
                    'PageNamespaceFacet': {
                        'type': 'string', 
                        'path': 'PageNamespace'
                    }, 
                    'SiteInfoNameFacet': {
                        'type': 'string', 
                        'path': 'SiteInfoName'
                    }, 
                    'SiteInfoDBNameFacet': {
                        'type': 'string', 
                        'path': 'SiteInfoDBName'
                    }, 
                    'SiteLanguageFacet': {
                        'type': 'string', 
                        'path': 'SiteLanguage'
                    }, 
                    'PageRestrictionsFacet': {
                        'type': 'string', 
                        'path': 'PageRestrictions'
                    },
                      'PageBytesFacet': {
                        'type': 'number', 
                        'path': 'PageBytes',
                        'boundaries': [0, 30000, 60000, 90000, 120000, 150000, 180000, 210000, 240000, 270000, 300000],
                        "default": "+300000"
                    }, 
                      'PageNumberLinksFacet': {
                        'type': 'number', 
                        'path': 'PageNumberLinks',
                        'boundaries': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                        "default": "+50"
                    },
                      "PageLastModifiedFacet": {
                        "type": "date",
                        "path": "PageLastModified",
                        "boundaries": [ 
                            dt.datetime(2023, 1, 1, 0, 0, 0),
                            dt.datetime(2023, 2, 1, 0, 0, 0),
                            dt.datetime(2023, 3, 1, 0, 0, 0),
                            dt.datetime(2023, 4, 1, 0, 0, 0),
                            dt.datetime(2023, 5, 1, 0, 0, 0),
                            dt.datetime(2023, 6, 1, 0, 0, 0),
                            dt.datetime(2023, 7, 1, 0, 0, 0),
                            dt.datetime(2023, 8, 1, 0, 0, 0),
                            dt.datetime(2023, 9, 1, 0, 0, 0),
                            dt.datetime(2023, 10, 1, 0, 0, 0),
                            dt.datetime(2023, 11, 1, 0, 0, 0),
                            dt.datetime(2023, 12, 1, 0, 0, 0)
                        ],
                        "default": "Older"
                    }, 
                      'PageHasRedirectFacet': {
                        'type': 'string', 
                        'path': 'PageHasRedirect',
                    }
                }
            }, 
            'highlight': {
                'path': {
                    'wildcard': '*'
                },
                "maxNumPassages": 1
            }
        }
    }, {
        '$facet': {
            'docs': [
                { 
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "PageBytes": 1,
                        "PageHasRedirect": 1,
                        "PageId": 1,
                        "PageLastModified": 1,
                        "PageLastModifiedUser": 1,
                        "PageLinks": 1,
                        "PageNamespace": 1,
                        "PageNumberLinks": 1,
                        "PageRedirect": 1,
                        "PageRestrictions": 1,
                        "PageText": 1,
                        "PageTitle": 1,
                        "PageWikipediaLink": 1,
                        "SiteInfoDBName": 1,
                        "SiteInfoName": 1,
                        "SiteLanguage": 1,
                        "pageWikipediaGenerated": 1,
                        "highlights": { "$meta": "searchHighlights" }
                    }
                }, {
                    "$limit": 500
                }
            ], 
            'facets': [
                {
                    '$replaceWith': '$$SEARCH_META'
                }, {
                    '$limit': 1
                },
            ]
        }
    }
]   
    if searchQuery.isnumeric():
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageBytes", "value": int(searchQuery)}})
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageId", "value": int(searchQuery)}})
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageNumberLinks", "value": int(searchQuery)}})
    elif isValidDate(searchQuery):
      pipeline[0]["$search"]["facet"]["operator"]["compound"]["should"].append({"equals": {"path": "PageLastModified", "value": dt.datetime.strptime(searchQuery, "%Y-%m-%d")}}) 
    return pipeline

def filteredTextSearchQuery(searchQuery, PageLastModifiedUser, PageNamespace, SiteInfoName, SiteInfoDBName, SiteLanguage, PageRestrictions, PageBytes, PageNumberLinks, PageLastModified, PageHasRedirect):
    pipeline = textSearchQuery(searchQuery)
    if PageLastModifiedUser:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageLastModifiedUser", "query": PageLastModifiedUser}})
    if PageNamespace:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageNamespace", "query": PageNamespace}})
    if SiteInfoName:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "SiteInfoName", "query": SiteInfoName}})
    if SiteInfoDBName:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "SiteInfoDBName", "query": SiteInfoDBName}})
    if SiteLanguage:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "SiteLanguage", "query": SiteLanguage}})
    if PageRestrictions:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageRestrictions", "query": PageRestrictions}})
    if PageBytes:
        if PageBytes == "+300000":
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageBytes", "gte": 300000}})
        else:
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageBytes", "lt": (int(PageBytes)+30000), "gte": int(PageBytes)}})
    if PageNumberLinks:
        if PageNumberLinks == "+50":
                pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageNumberLinks", "gte": 50}})
        else:
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageNumberLinks", "lt": (int(PageNumberLinks)+5), "gte": int(PageNumberLinks)}})
    if PageLastModified:
        if PageLastModified == "Older":
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageLastModified", "lte": dt.datetime(2023, 1, 1, 0, 0, 0)}})
        else: 
            date_format = "%a, %d %b %Y %H:%M:%S %Z"
            # Parse the date string into a datetime object
            dateObj = dt.datetime.strptime(PageLastModified, date_format)
            newDate = dateObj + dt.timedelta(days=31)
            pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"range": {"path": "PageLastModified", "lt": newDate, "gte": dateObj}})
    if PageHasRedirect:
        pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "PageHasRedirect", "query": PageHasRedirect}})
    return pipeline

@app.route("/")
def home():
    return render_template_string('''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="css url"/>
    </head>
    <body>
        <p>Aplicación de Mongo!</p>
    </body>
</html>
''')

# Código basado de 
# https://stackoverflow.com/questions/58676559/how-to-authenticate-to-firebase-using-python/71398321#71398321
# https://datagy.io/python-requests-response-object/

@app.route("/login", methods=["POST"]) 
def login():
    if request.method == "POST":
        REQUEST_COUNT.inc()
    
        data = request.get_json()
        try:
            
            email =data["email"]
            password = data["password"]
            logger.debug(email)
            logger.debug(password)
            userInfo = json.dumps({"email": email, "password": password, "return_secure_token":True})
            r = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAFj0oFcEqOdCL1NFlbGVhvirpxrKqx_LY", userInfo)
            logger.debug(r)
            if r:
                logger.debug("El usuario sí existe")
            else:
                logger.debug("El usuario no existe")
            logger.debug(r.json())
            return r.json()
        except Exception as e:
            logger.debug("Ese correo electrónico no está registado", e)
        return json.dumps({"error": {"code": 500, "message": "ERROR"}})

@app.route("/register", methods=["POST"]) 
def register():
    if request.method == "POST":
        REQUEST_COUNT.inc()
        data = request.get_json()
        pEmail = data["email"]
        pPassword = data["password"]
        pPhone = data["phone"]
        pDisplayName = data["name"] + " " + data["last_name1"] + " " + data["last_name2"]        
        try:
            user = auth.create_user(email = pEmail, password = pPassword, phone_number = pPhone, display_name = pDisplayName)
            return {"success": {"code": 200, "message": "The user has been registered correctly"}}
        except Exception as e:
            logger.debug(str(e))
            logger.debug("El usuario ya está registrado.", e)
            return json.dumps({"error": {"code": 500, "message": "The user has already been registered"}})    
    
@app.route("/mongodb/get_data/<query>", methods=["POST"])
def get_data (query):
    REQUEST_COUNT.inc()
    filters = request.get_json()
    record = {'logId': int(time.time()) + random.randint(0, 30000), 'title': "get_data", 'bagInfo': json.dumps({"query": query, "body": filters})}
    write_a_record(handle, 'ic4302_logs', record)
    pipeline = filteredTextSearchQuery(query, filters[0], filters[1], filters[2], filters[3], filters[4], filters[5], filters[6], filters[7], filters[8], filters[9])
    results = list(mongo.db.pages.aggregate(pipeline))[0]
    for doc in results["docs"]:
        for highlight in doc["highlights"]:
            doc[highlight["path"]] = highlight["texts"]
    # logger.debug(results)
    
    return results

@app.route("/mongodb/update_vote/<id>/<vote>", methods=["POST"])
def upsertVote(id, vote):
    REQUEST_COUNT.inc()
    record = {'logId': int(time.time()) + random.randint(0, 30000), 'title': "update_vote", 'bagInfo': json.dumps({"id": id, "vote": vote})}
    write_a_record(handle, 'ic4302_logs', record)
    try:
        query = {"_id": id}
        voteVal = int(vote)
        update = {'$inc': {'PagePoints': 1}} if voteVal else {'$inc': {'PagePoint': -1}}
        mongo.db.pages.update_one(query, update, upsert= True)
        return jsonify("Updated the points on the document. ")
    except Exception as e:
        raise e

@app.route("/mongodb/get_doc/<id>/<query>", methods=["POST"])
def get_doc (id, query):
    REQUEST_COUNT.inc()
    record = {'logId': int(time.time()) + random.randint(0, 30000), 'title': "get_doc", 'bagInfo': json.dumps({"id": id, "query": query})}
    write_a_record(handle, 'ic4302_logs', record)
    pipeline = textSearchQuery(query)
    pipeline[0]["$search"]["facet"]["operator"]["compound"]["filter"].append({"phrase": {"path": "_id", "query": id}})
    document = list(mongo.db.pages.aggregate(pipeline))[0]["docs"][0]
    toHighlight = []
    for dict in document["highlights"]:  
        toHighlight.append(dict["path"])
    toHighlight.remove("_id")

    for path in toHighlight:
        if isinstance(document[path], str):
            text = document[path].split()
            document[path] = []
            for word in text:
                if word.lower() == query.lower():
                    document[path].append({"type": "hit", "value": word})
                else:
                    document[path].append({"type": "text", "value": word})
    return document

@app.route('/autonomous/update_pagepoints/<pageId>', methods=['PUT'])
def update_pagepoints(pageId):
    REQUEST_COUNT.inc()

    value = request.json['value']

    cur = autonomous.cursor()

    params = [pageId, value]

    # Call the procedure using the list of parameters
    cur.callproc('update_pagepoints', params)
    
    points = getAutonomousPoints(pageId)
    
    return str(points)



@app.route('/autonomous/get_pages_facets/', methods=['POST'])
def get_pages_facets():
    REQUEST_COUNT.inc()
    
    filters = request.get_json()
    
    search = searchAutonomousWithFacets(filters[0], filters[1], filters[2], filters[3], filters[4], filters[5], filters[6], filters[7], filters[8], filters[9])

    return search


@app.route('/autonomous/get_pages/<query>', methods=['GET'])
def get_pages(query):
    
    createAutonomousView(query)
    pages = []
    pages = searchAutonomous()

    return pages


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    
    mongo = mongoDBConnection()
    autonomous = connectAutonomousDB()

    start_http_server(8000)
    app.run(debug = True)
    