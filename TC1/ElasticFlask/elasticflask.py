from flask import Flask, request

app = Flask(__name__)
pokemon = []

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

@app.route("/deletePokemon", methods=["POST", "GET"]) 
def delete():
    if request.method == "POST":
        print(request.form)
        print(request.form["Name"])
        return pokemon

if __name__ == "__main__":
    app.run(debug=True)