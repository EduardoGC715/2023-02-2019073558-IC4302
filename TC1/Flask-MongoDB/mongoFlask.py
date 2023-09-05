from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# código basado en https://pypi.org/project/pg8000/#installation
app = Flask(__name__)
pokemon = []
logger.debug('mongodb://' + environ['MONGODB_USERNAME'] + ':' + environ['MONGODB_PASSWORD'] + '@' + environ['MONGODB_HOSTNAME'] + ':27017/' + environ['MONGODB_DATABASE'])
app.config["MONGO_URI"] = 'mongodb://' + environ['MONGODB_USERNAME'] + ':' + environ['MONGODB_PASSWORD'] + '@' + environ['MONGODB_HOSTNAME'] + ':27017/' + environ['MONGODB_DATABASE']

mongo = PyMongo(app)
db = mongo.db
logger.debug(mongo)
logger.debug(db)
if mongo.db.client:
    logger.debug("Connected to MongoDB successfully!")


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

@app.route("/getPokemon/<id>", methods=["POST", "GET"])
def getOnePokemon(id):
    if request.method == "GET":
        try:
            pokemonFound = db.pokemon.find_one({"Id": id})
            logger.debug(f"Get One: {pokemonFound}")
            return f"Get one {pokemonFound}"
        except Exception as e:
            logger.debug("No se pudo encontrar el pokemon: ", e)
        

@app.route("/getAllPokemon", methods=["POST", "GET"])
def getAllPokemon():
    if request.method == "GET":
        pokemones = db.pokemon.find()
        pokemonGet = []
        for species in pokemones:
            item = {
            "Id": str(species["Id"]),
            "Name": str(species["Name"]),
            "Type1": str(species["Type1"]),
            "Type2": str(species["Type2"]),
            "Category": str(species["Category"]),
            "Heightf": str(species["Heightf"]),
            "Heightm": str(species["Heightm"]),
            "Weightlbs": str(species["Weightlbs"]),
            "Weightkg": str(species["Weightkg"]),
            "CaptureRate": str(species["CaptureRate"]),
            "EggSteps": str(species["EggSteps"]),
            "ExpGroup": str(species["ExpGroup"]),
            "Total": str(species["Total"]),
            "HP": str(species["HP"]),
            "Attack": str(species["Attack"]),
            "Defense": str(species["Defense"]),
            "SpAttack": str(species["SpAttack"]),
            "SpDefense": str(species["SpDefense"]),
            "Speed": str(species["Speed"])
            }
            pokemonGet.append(item)
        logger.debug(f"Pokemones Get All {pokemonGet}")
        return f"Pokemones Get All {pokemonGet}"


@app.route("/postPokemon", methods=["POST"]) 
def insertPokemon():
    if request.method == "POST":
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

@app.route("/deletePokemon/<id>", methods=["DELETE"]) 
def delete(id):
    if request.method == "DELETE":
        try:
            pokemonFound = db.pokemon.delete_one({"Id": id})
            logger.debug(f"Delete One: {pokemonFound}")
            return f"Delete one {pokemonFound}"
        except Exception as e:
            logger.debug("No se pudo eliminar el pokemon: ", e)
            return f"Delete failed"
            


if __name__ == "__main__":
    
    app.run(debug=True)