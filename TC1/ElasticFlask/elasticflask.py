from flask import Flask, request, render_template_string
import os
import logging
import json
from elasticsearch import Elasticsearch
from prometheus_client import start_http_server, Counter

# Página usada como referencia para el código de elasticsearch: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html
# https://github.com/prometheus/client_python

# Create a metric to http requests made.
REQUEST_COUNT = Counter('flask_http_requests', 'Number of HTTP requests received')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Parámetros de conexión a Elasticsearch
ESUSERNAME = os.getenv('ESUSERNAME')
ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD = os.getenv('ESPASSWORD')
ESINDEX = os.getenv('ESINDEX')

try:
    es = Elasticsearch("http://" + ESENDPOINT + ":9200", basic_auth=(ESUSERNAME, ESPASSWORD), verify_certs=False)
    logger.debug('Elasticsearch at http://' + ESENDPOINT + ":9200 connected")

    # Crea el índice de pokemones, o el dado en ESINDEX
    # Código de referencia: https://kb.objectrocket.com/elasticsearch/how-to-create-and-delete-elasticsearch-indexes-using-the-python-client-library
    try:
        es.indices.create(index=ESINDEX)
        logger.debug(f"Index '{ESINDEX}' created successfully.")
    except Exception as e:
        logger.error(e)
        logger.debug(f"Index '{ESINDEX}' already exists.")

except Exception as e:
    logger.error(e)



@app.route("/")
def home():
    return render_template_string('''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="css url"/>
    </head>
    <body>
        <p>Aplicación de Elasticsearch!</p>
    </body>
</html>
''')

@app.route("/getPokemon/<id>", methods=["GET"])
def getOnePokemon(id):
    if request.method == "GET":
        REQUEST_COUNT.inc()
        try:
            results = es.search(index=ESINDEX, query={"term":  { "Id": id}})
            if len(results['hits']['hits']) != 0:
                pokemonFound = results["hits"]["hits"][0]["_source"]["Id"]
                logger.debug(f"Get One: {pokemonFound}")
                return f"Get one {pokemonFound}"
            else:
                logger.debug(f"Pokemon {id} not found")
                return f"Pokemon {id} not found"
        except Exception as e:
            logger.debug("No se pudo encontrar el pokemon: ", e)

@app.route("/getAllPokemon", methods=["GET"])
def getAllPokemon():
    if request.method == "GET":
        REQUEST_COUNT.inc()
        pokemones = es.search(index=ESINDEX, query={"match_all": {}})
        pokemonGet = len(pokemones["hits"]["hits"])
        logger.debug(f"Pokemones Get All {pokemonGet}")
        return f"Pokemones Get All {pokemonGet}"

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
        try:
            es.index(index=ESINDEX, document = json.dumps(formPokemon))
            logger.debug(f"Pokemon Post {formPokemon}")
        except Exception as e:
            logger.debug("No se pudo insertar. ", e)
        return f"Pokemon {formPokemon}"

@app.route("/putPokemon/<id>", methods=["PUT"]) 
def updatePokemon(id):
    if request.method == "PUT":
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
        
        try:
            results = es.search(index=ESINDEX, query={"term":  { "Id": id}}, size=1)
            if len(results['hits']['hits']) != 0:
                pokemonFound = results["hits"]["hits"][0]
                es.update(index=ESINDEX, id=pokemonFound['_id'], doc=formPokemon, refresh = True)
                logger.debug(f"Pokemon Update {pokemonFound['_source']['Id']}")
                return f"Update one {pokemonFound['_source']['Id']}"
            else:
                logger.debug(f"Pokemon {id} not found. Not updated.")
                return f"Pokemon {id} not found. Not updated."
        except Exception as e:
            logger.debug("No se pudo actualizar. ", e)
        return f"Pokemon Update {formPokemon['Id']} failed"

# borrar pokemon
@app.route("/deletePokemon/<id>", methods=["DELETE"]) 
def delete(id):
    if request.method == "DELETE":
        REQUEST_COUNT.inc()
        try:
            # buscamos el pokemon
            results = es.search(index=ESINDEX, query={"term":  { "Id": id}}, size=1)
            if len(results['hits']['hits']) != 0:
                # si lo encuentra, lo borra
                pokemonFound = results["hits"]["hits"][0]
                delete_result = es.delete(index=ESINDEX, id=pokemonFound['_id'])
                if delete_result['result'] == "deleted":
                    logger.debug(f"Pokemon Delete {pokemonFound['_source']['Id']}")
                    return f"Delete one {pokemonFound['_source']['Id']}"
                else:
                    logger.debug(f"Couldn't delete Pokemon {id}")
                    return f"Couldn't delete Pokemon {id}"
            else:
                logger.debug(f"Pokemon {id} not found. Not deleted.")
                return f"Pokemon {id} not found. Not deleted."
        except Exception as e:
            logger.debug("No se pudo eliminar pokemon: ", e)
            return f"Delete failed"
            


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    app.run()
    