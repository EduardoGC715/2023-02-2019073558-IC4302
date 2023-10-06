import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("bibliotec-98a06-firebase-adminsdk-qiahh-ea76f83463.json")
firebase_admin.initialize_app(cred)

import bson
from flask import Flask, request, render_template_string, current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from os import environ
import logging
from prometheus_client import start_http_server, Counter
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
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
uri = "mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/?retryWrites=true&w=majority"

# Código basado en

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Conexión con MongoDB exitosa")
except Exception as e:
    print(e)

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

@app.route("/getMongo/", methods=["GET"])
def getFromMongo():
    if request.method == "GET":
        REQUEST_COUNT.inc()
        
        form = {
            
        }
        try:
            pokemonFound = db.find_one({"Id": id})
            logger.debug(f"Get One:")
            return f"Get one "
        except Exception as e:
            logger.debug("No se pudo encontrar el pokemon: ", e)
    record = {'logId': int(time.time()) + random.randint(0, 30000), 'title': "test", 'bagInfo': json.dumps({"id": 1, "text": "test"})}
    write_a_record(handle, 'ic4302_logs', record)       

@app.route("/getAutonomous", methods=["GET"])
def getFromAutonomous():
    if request.method == "GET":
        REQUEST_COUNT.inc()
        pokemones = db.pokemon.find()
        
        logger.debug(f"Pokemones Get All")
        return f"Pokemones Get All"

# Código basado de 
# https://stackoverflow.com/questions/58676559/how-to-authenticate-to-firebase-using-python/71398321#71398321
# https://datagy.io/python-requests-response-object/
# https://firebase.google.com/docs/reference/rest/auth
# https://firebase.google.com/docs/auth/admin/manage-users

@app.route("/login", methods=["POST"]) 
def login():
    if request.method == "POST":
        REQUEST_COUNT.inc()        
        try:
            email =request.form["email"]
            password = request.form["password"]
            userInfo = json.dumps({"email": email, "password": password, "return_secure_token":True})
            r = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAFj0oFcEqOdCL1NFlbGVhvirpxrKqx_LY", userInfo)
            if r:
                logger.debug("El usuario sí existe")
            else:
                logger.debug("El usuario no existe")
        except Exception as e:
            logger.debug("Ese correo electrónico no está registado", e)
        return f"Pokemon"

@app.route("/register", methods=["POST"]) 
def register():
    if request.method == "POST":
        logger.debug("Llegó el request")
        REQUEST_COUNT.inc()
        pEmail = request.form["email"]
        pPassword = request.form["password"]
        pPhone = request.form["phone"]
        pDisplayName = request.form["name"] + " " + request.form["last_name1"] + " " + request.form["last_name2"]        
        try:
            user = auth.create_user(email = pEmail, password = pPassword, phone_number = pPhone, display_name = pDisplayName)
        except Exception as e:
            logger.debug(str(e))
            logger.debug("El usuario ya está registrado.", e)
        return "Usuario registrado"



            

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    
    app.config['MONGO_URI']  = uri
    start_http_server(8000)
    app.run()
    