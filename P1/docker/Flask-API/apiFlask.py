import bson
from flask import Flask, request, render_template_string, current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from os import environ
import logging
from prometheus_client import start_http_server, Counter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


uri = "mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

# Codigo basado en https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
# https://github.com/prometheus/client_python

# Create a metric to track time spent and requests made.
REQUEST_COUNT = Counter('flask_http_requests', 'Number of HTTP requests received')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 
app = Flask(__name__)
"""
pokemon = []
# logger.debug('mongodb://' + environ['MONGODB_USERNAME'] + ':' + environ['MONGODB_PASSWORD'] + '@' + environ['MONGODB_HOSTNAME'] + ':27017/' + environ['MONGODB_DATABASE'])
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)
db = mongo.db
logger.debug(mongo)
logger.debug(db)
if mongo.db.client:
    logger.debug("Connected to MongoDB successfully!")
"""

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

@app.route("/getPokemon/<id>", methods=["GET"])
def getOnePokemon(id):
    if request.method == "GET":
        REQUEST_COUNT.inc()
        try:
            pokemonFound = db.pokemon.find_one({"Id": id})
            logger.debug(f"Get One:")
            return f"Get one "
        except Exception as e:
            logger.debug("No se pudo encontrar el pokemon: ", e)

@app.route("/getAllPokemon", methods=["GET"])
def getAllPokemon():
    if request.method == "GET":
        REQUEST_COUNT.inc()
        pokemones = db.pokemon.find()
        
        logger.debug(f"Pokemones Get All")
        return f"Pokemones Get All"

@app.route("/postPokemon", methods=["POST"]) 
def insertPokemon():
    if request.method == "POST":
        REQUEST_COUNT.inc()
        formPokemon = {
        "Id": request.form["Id"],
        "Name": request.form["Name"],
        "Type1": request.form["Type1"],
        "Type2": request.form["Type2"],
        "Category": request.form["Category"],
        "Heightf": request.form["Heightf"],
        "Heightm": request.form["Heightm"],
        "Weightlbs": request.form["Weightlbs"],
        "Weightkg": request.form["Weightkg"],
        "CaptureRate": request.form["CaptureRate"],
        "EggSteps": request.form["EggSteps"],
        "ExpGroup": request.form["ExpGroup"],
        "Total": request.form["Total"],
        "HP": request.form["HP"],
        "Attack": request.form["Attack"],
        "Defense": request.form["Defense"],
        "SpAttack": request.form["SpAttack"],
        "SpDefense": request.form["SpDefense"],
        "Speed": request.form["Speed"]
        }
        pokemon.append(formPokemon)
        try:
            db.pokemon.insert_one(formPokemon)
            logger.debug(f"Pokemon Post {formPokemon}")
        except Exception as e:
            logger.debug("No se pudo insertar. ", e)
        return f"Pokemon {formPokemon}"

@app.route("/putPokemon/<id>", methods=["PUT"]) 
def updatePokemon(id):
    if request.method == "PUT":
        REQUEST_COUNT.inc()
        formPokemon = {"$set": {
        "Id": request.form["Id"],
        "Name": request.form["Name"],
        "Type1": request.form["Type1"],
        "Type2": request.form["Type2"],
        "Category": request.form["Category"],
        "Heightf": request.form["Heightf"],
        "Heightm": request.form["Heightm"],
        "Weightlbs": request.form["Weightlbs"],
        "Weightkg": request.form["Weightkg"],
        "CaptureRate": request.form["CaptureRate"],
        "EggSteps": request.form["EggSteps"],
        "ExpGroup": request.form["ExpGroup"],
        "Total": request.form["Total"],
        "HP": request.form["HP"],
        "Attack": request.form["Attack"],
        "Defense": request.form["Defense"],
        "SpAttack": request.form["SpAttack"],
        "SpDefense": request.form["SpDefense"],
        "Speed": request.form["Speed"]
        }}
        
        try:
            db.pokemon.update_one({"Id": id}, formPokemon)
            logger.debug(f"Pokemon Update {formPokemon['$set']}")
        except Exception as e:
            logger.debug("No se pudo actualizar. ", e)
        return f"Pokemon Update {formPokemon['$set']}"


            

if __name__ == "__main__":
    # Start up the server to expose the metrics.
    
    app.config['MONGO_URI']  = uri
    start_http_server(8000)
    app.run()
    