from flask import Flask, request, redirect, url_for, render_template
import json

app = Flask(__name__)
pokemon = [
#   {
#     "Id": "#{Id}",
#     "Name": "#{Name}",
#     "Type1": "#{Type1}",
#     "Type2": "#{Type2}",
#     "Category": "#{Category}",
#     "Heightf": "#{Heightf}",
#     "Heightm": "#{Heightm}",
#     "Weightlbs": "#{Weightlbs}",
#     "Weightkg": "#{Weightkg}",
#     "CaptureRate": "#{CaptureRate}",
#     "EggSteps": "#{EggSteps}",
#     "ExpGroup": "#{ExpGroup}",
#     "Total": "#{Total}",
#     "HP": "#{HP}",
#     "Attack": "#{Attack}",
#     "Defense": "#{Defense}",
#     "SpAttack": "#{SpAttack}",
#     "SpDefense": "#{SpDefense}",
#     "Speed": "#{Speed}"
#   }
]

@app.route("/")
def home():
    return

@app.route("/getPokemon", methods=["POST", "GET"])
def get():
    print(pokemon)
    return pokemon


@app.route("/postPokemon", methods=["POST", "GET"]) 
def post():
    if request.method == "POST":
        print(request.get_json())
        pokemon.append(request.get_json())
        return pokemon

@app.route("/deletePokemon", methods=["POST", "GET"]) 
def delete():
    pass

if __name__ == "__main__":
    app.run(debug=True)