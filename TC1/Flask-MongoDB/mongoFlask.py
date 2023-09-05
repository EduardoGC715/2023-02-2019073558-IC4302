from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo
from os import environ
import jsonify
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
print(mongo)
print(db)
if mongo.db.client:
    print("Connected to MongoDB successfully!")


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
    try:
        pokemonFound = db.pokemon.find_one({"Id": id})
        print(pokemonFound)
        return f"Pokemon {pokemonFound}!"
    except Exception as e:
        print("No se pudo encontrar el pokemon: ", e)

@app.route("/getAllPokemon", methods=["POST", "GET"])
def getAllPokemon():
    
    return pokemon


@app.route("/postPokemon", methods=["POST", "GET"]) 
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
        print(formPokemon)
        pokemon.append(formPokemon)
        try:
            db.pokemon.insert_one(formPokemon)
        except Exception as e:
            print("No se pudo insertar. ", e)
        return f"Pokemon {formPokemon}!"

@app.route("/putPokemon", methods=["POST", "GET"]) 
def updatePokemon():
    if request.method == "POST":
        print(request.form)
        print(request.form["Name"])
        formPokemon = [
        {
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
        ]
        pokemon.append(formPokemon)
        return formPokemon

@app.route("/deletePokemon/<id>", methods=["POST", "GET"]) 
def delete(id):
    if request.method == "POST":
        print(request.form)
        print(request.form["Name"])
        return pokemon

if __name__ == "__main__":
    
    app.run(debug=True)