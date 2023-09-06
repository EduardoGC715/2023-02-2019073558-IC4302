from flask import Flask, request, jsonify
import pg8000.native
from os import environ
import logging

# código basado en https://pypi.org/project/pg8000/#installation
app = Flask(__name__)

# Function to connect to PostGreSQL

def connectPostGreSQL():
    try:
        databasePG = environ.get("PGDATABASE")
        username = environ.get("PGUSER")
        passwordPG = environ.get("PGPASSWORD")
        servicePG = environ.get("PGSERVICE")
        logger.debug(databasePG)
        logger.debug(username)
        logger.debug(passwordPG)
        logger.debug(servicePG)
        
        conn = pg8000.native.Connection(username, password=passwordPG, host=servicePG, database=databasePG)
        return conn
    except Exception as e:
        logger.error(e)
        return None
        
def disconnectPostGreSQL(conn):
    try:
        conn.close()
    except Exception as e:
        logger.error(e)

def createTablePostGreSQL(conn):
    try:
        tableName = "pokemons"

        createTableQuery = f"""
            CREATE TABLE IF NOT EXISTS {tableName} (
                primaryKey SERIAL PRIMARY KEY,
                pokemonId VARCHAR(255),
                PokemonName VARCHAR(255),
                Type1 VARCHAR(255),
                Type2 VARCHAR(255),
                Category VARCHAR(255),
                Heightf VARCHAR(255),
                Heightm VARCHAR(255),
                Weightlbs VARCHAR(255),
                Weightkg VARCHAR(255),
                CaptureRate VARCHAR(255),
                EggSteps VARCHAR(255),
                ExpGroup VARCHAR(255),
                Total VARCHAR(255),
                HP VARCHAR(255),
                Attack VARCHAR(255),
                Defense VARCHAR(255),
                SpAttack VARCHAR(255),
                SpDefense VARCHAR(255),
                Speed VARCHAR(255)
            )
            """
        conn.run(createTableQuery)
        logger.debug("Table created...")

    except Exception as e:
        logger.error(e)

@app.route("/")
def home():
    return "<h1>PostGreSQL Flask App</h1>"

@app.route('/test')
def test():
    return 'Hello World! I am the PostGreSQL Flask app!'

@app.route('/test_db')
def test_db():
    databasePG = environ.get("PGDATABASE")
    username = environ.get("PGUSER")
    passwordPG = environ.get("PGPASSWORD")
    servicePG = environ.get("PGSERVICE")
    logger.debug(databasePG)
    logger.debug(username)
    logger.debug(passwordPG)
    logger.debug(servicePG)

    con = pg8000.native.Connection(username, password=passwordPG, host=servicePG, database=databasePG)
    # Create a temporary table
    con.run("CREATE TEMPORARY TABLE book (id SERIAL, title TEXT)")

    # Populate the table
    for title in ("Ender's Game", "The Magus"):
        con.run("INSERT INTO book (title) VALUES (:title)", title=title)

    # Print all the rows in the table  
    for row in con.run("SELECT * FROM book"):
        print(row)
    con.close()
    return "<h1> Connected successfully. </h1>"

@app.route("/getPokemon/<id>", methods=["GET"])
def getPokemon(id):
    pass

@app.route("/getAllPokemon", methods=["GET"])
def getAllPokemon():
    pass

@app.route("/postPokemon", methods=["POST"])
def postPokemon():
    global conn

    try:
        data = request.get_json()
        insertQuery = """
            INSERT INTO pokemons (pokemonId, PokemonName, Type1, Type2, Category, Heightf, Heightm, Weightlbs, Weightkg, CaptureRate, EggSteps, ExpGroup, Total, HP, Attack, Defense, SpAttack, SpDefense, Speed)
            VALUES
            (:pokemonId, :PokemonName, :Type1, :Type2, :Category, :Heightf, :Heightm, :Weightlbs, :Weightkg, :CaptureRate, :EggSteps, :ExpGroup, :Total, :HP, :Attack, :Defense, :SpAttack, :SpDefense, :Speed)
            """
        conn.run(insertQuery,
                pokemonId = data["Id"],
                PokemonName = data["Name"],
                Type1 = data["Type1"],
                Type2 = data["Type2"],
                Category = data["Category"],
                Heightf = data["Heightf"],
                Heightm = data["Heightm"],
                Weightlbs = data["Weightlbs"],
                Weightkg = data["Weightkg"],
                CaptureRate = data["CaptureRate"],
                EggSteps = data["EggSteps"],
                ExpGroup = data["ExpGroup"],
                Total = data["Total"],
                HP = data["HP"],
                Attack = data["Attack"],
                Defense = data["Defense"],
                SpAttack = data["SpAttack"],
                SpDefense = data["SpDefense"],
                Speed = data["Speed"]
                )
        logger.debug(f"Inserted {data['Id']} Name: {data['Name']}")
    except Exception as e:
        logger.error(e)
    

@app.route("/putPokemon/<id>", methods=["PUT"])
def putPokemon(id):
    pass

@app.route("/deletePokemon/<id>", methods=["DELETE"])
def deletePokemon(id):
    pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    conn = connectPostGreSQL()
    createTablePostGreSQL(conn)
    app.run()