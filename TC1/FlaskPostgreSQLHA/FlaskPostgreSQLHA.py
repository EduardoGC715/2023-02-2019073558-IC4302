import pg8000.native as pg
import os
from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Counter
import logging

app = Flask(__name__)

REQUEST_COUNT = Counter('flask_http_requests', 'Number of HTTP requests received')

# Function to connect to PostgreSQL using pg8000
def connectPostgreSQL():
    try:
        # Replace with your PostgreSQL connection parameters
        host = os.environ.get("PG_HOST")
        port = 5432  # Change the port if necessary
        database = os.environ.get("PG_DATABASE")
        user = os.environ.get("PG_USER")
        password = os.environ.get("PG_PASSWORD")

        # Create a connection to the PostgreSQL database
        conn = pg.Connection(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        return conn
    except Exception as e:
        # Handle the exception
        logger.debug(f"Error connecting to PostgreSQL: {e}")
        return None
    
# Function to disconnect from PostgreSQL using pg8000
def disconnectPostgreSQL(conn):
    try:
        conn.close()
    except Exception as e:
        # Handle the exception
        logger.error(f"Error closing PostgreSQL connection: {e}")

# Function to create a PostgreSQL table for storing Pokemon using pg8000
def createTablePostgreSQL(conn):
    try:

        # Define the table name (replace 'your_table' with your preferred table name)
        tableName = 'pokemons'

        # Define the SQL CREATE TABLE statement
        createTableQuery = f"""
        CREATE TABLE {tableName} (
            PokemonId SERIAL PRIMARY KEY,
            Id VARCHAR(255),
            Name VARCHAR(255),
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
        
        # Execute the CREATE TABLE statement
        conn.run(createTableQuery)

        logger.debug(f"Table '{tableName}' created successfully.")
    except Exception as e:
        # Handle the exception
        logger.error(f"Error creating table: {e}")

# Function to transform a JSON query into a SQL query for INSERT in PostgreSQL using pg8000
def dictToSQLInsert(data, tableName, columns):
    try:
        # Extract values from the data dictionary in the same order as the columns
        values = [f"'{data[column]}'" for column in columns]

        # Construct the SQL INSERT statement
        setClauseColumns = "(" + ', '.join(columns) + ")"
        setClauseValues = "(" + ', '.join(values) + ")"
        insertQuery = f"INSERT INTO {tableName} {setClauseColumns} VALUES {setClauseValues}"

        return insertQuery
    except Exception as e:
        raise Exception(f"Error transforming data to SQLInsert: {e}")

# Function to transform a dictionary into a SQL UPDATE statement for PostgreSQL using pg8000
def dictToSQLUpdate(tableName, id, data):
    try:

        # Construct the SQL UPDATE statement
        setClause = ", ".join([f"{column} = '{value}'" for column, value in data.items()])
        updateQuery = f"UPDATE {tableName} SET {setClause} WHERE PokemonId = (SELECT PokemonId FROM pokemons WHERE Id = \'{id}\' LIMIT 1);"

    except Exception as e:
        raise Exception("Error transforming data to SQLUpdate: " + str(e))
    
@app.route("/postPokemon", methods=['POST'])
def postData():
    try:
        REQUEST_COUNT.inc()

        # Connect to the PostgreSQL database
        conn = connectPostgreSQL()  # Use the PostgreSQL connection function

        # Define the table to insert to (adjust table name as needed)
        data = {
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
            "Speed": request.form["Speed"]}

        insertQuery = """
                INSERT INTO pokemons (Id, Name, Type1, Type2, Category, Heightf, Heightm, Weightlbs, Weightkg, CaptureRate, EggSteps, ExpGroup, Total, HP, Attack, Defense, SpAttack, SpDefense, Speed)
                VALUES
                (:Id, :Name, :Type1, :Type2, :Category, :Heightf, :Heightm, :Weightlbs, :Weightkg, :CaptureRate, :EggSteps, :ExpGroup, :Total, :HP, :Attack, :Defense, :SpAttack, :SpDefense, :Speed)
                """
        conn.run("SET default_transaction_read_only = OFF")   
        conn.run(insertQuery,
                Id = data["Id"],
                Name = data["Name"],
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

        disconnectPostgreSQL(conn)

        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/deletePokemon/<id>", methods=['DELETE'])
def deleteData(id):
    try:
        REQUEST_COUNT.inc()
        # Connect to the PostgreSQL database
        conn = connectPostgreSQL()  # Use the PostgreSQL connection function

        conn.run("DELETE FROM pokemons WHERE PokemonId = (SELECT PokemonId from Pokemons where Id = :Id LIMIT 1)", Id = id)

        disconnectPostgreSQL(conn)

        return jsonify({"message": "Data deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/putPokemon/<id>", methods=['PUT'])
def putData(id):
    try:
        REQUEST_COUNT.inc()

        # Connect to the PostgreSQL database
        conn = connectPostgreSQL()  # Use the PostgreSQL connection function

        # Execute the SQL UPDATE statement
        data = {
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
            "Speed": request.form["Speed"]}

        updateQuery = """
                UPDATE pokemons 
                SET Name = :Name,
                Type1 = :Type1,
                Type2 = :Type2,
                Category = :Category,
                Heightf = :Heightf,
                Heightm = :Heightm,
                Weightlbs = :Weightlbs,
                Weightkg = :Weightkg,
                CaptureRate = :CaptureRate,
                EggSteps = :EggSteps,
                ExpGroup = :ExpGroup,
                Total = :Total,
                HP = :HP,
                Attack = :Attack,
                Defense = :Defense,
                SpAttack = :SpAttack,
                SpDefense = :SpDefense,
                Speed = :Speed
                WHERE PokemonId = (SELECT PokemonId from Pokemons where Id = :Id LIMIT 1)
                """
        conn.run(updateQuery,
                    Id = id,
                    Name = data["Name"],
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

        disconnectPostgreSQL(conn)

        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/getAllPokemon", methods=['GET'])
def getAllData():
    try:
        REQUEST_COUNT.inc()
        # Connect to the PostgreSQL database
        conn = connectPostgreSQL()  # Use the PostgreSQL connection function

        # Define the table to query (adjust table name as needed)
        tableName = 'pokemons'

        # Construct the SELECT query
        select_query = ("SELECT * FROM "+tableName)

        # Execute the SELECT query using pg8000
        conn.run("SET default_transaction_read_only = OFF")
        result = conn.run(select_query)

        disconnectPostgreSQL(conn)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/getPokemon/<id>", methods=['GET'])
def getData(id):
    try:
        REQUEST_COUNT.inc()
        # Connect to the PostgreSQL database
        conn = connectPostgreSQL()  # Use the PostgreSQL connection function

        # Define the table to query (adjust table name as needed)
        tableName = 'pokemons'

        # Get the list of column names from the table schema
        columns = ["PokemonId",
            "Id",
            "Name",
            "Type1",
            "Type2",
            "Category",
            "Heightf",
            "Heightm",
            "Weightlbs",
            "Weightkg",
            "CaptureRate",
            "EggSteps",
            "ExpGroup",
            "Total",
            "HP",
            "Attack",
            "Defense",
            "SpAttack",
            "SpDefense",
            "Speed"]

        # Construct the SELECT query
        select_query = ("SELECT * FROM "+tableName+" WHERE PokemonId = "+str(id))

        # Execute the query
        conn.run("SET default_transaction_read_only = OFF")
        result = conn.run(select_query)
        result = result[0]

        conn.close()

        if result:
            # Create a dictionary with column names as keys
            data_dict = dict(zip(columns, result))
            return jsonify(data_dict), 200
        else:
            return jsonify({"error": "Record not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Connect to the PostgreSQL database and create the database and table if they don't exist
    conn = connectPostgreSQL()  # Use the PostgreSQL connection function
    conn.run("SET default_transaction_read_only = OFF")
    createTablePostgreSQL(conn)  # Use the PostgreSQL function to create the table if not exists
    disconnectPostgreSQL(conn)  # Disconnect from the PostgreSQL database

    # Run the Flask app
    start_http_server(8000)
    app.run()