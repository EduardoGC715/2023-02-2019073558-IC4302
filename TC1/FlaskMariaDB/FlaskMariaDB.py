import mariadb
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to connect to MariaDB
def connectMariaDB():
    try:
        conn = mariadb.connect(
            user=os.environ.get("MDB_USER"),
            password=os.environ.get("MDB_PASSWORD"),
            host=os.environ.get("MDB_HOST"),
            database=os.environ.get("MDB_DATABASE"),
        )
        return conn
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error connecting to MariaDB: {e}")
        return None

# Function to disconnect from MariaDB
def disconnectMariaDB(conn):
    try:
        conn.close()
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error closing MariaDB connection: {e}")

# Function to execute a given query on a given cursor connected to the database
def executeMariaDB(cursor, query):
    try:
        cursor.execute(query)
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error executing MariaDB query: {e}")

# Function to create a database for storing pokemon
def createDatabase():
    try:
        conn = mariadb.connect(
            user=os.environ.get("MDB_USER"),
            password=os.environ.get("MDB_PASSWORD"),
            host=os.environ.get("MDB_HOST")
        )
        cursor = conn.cursor()

        # Define the SQL CREATE DATABASE statement
        createDatabaseQuery = f"""
        CREATE DATABASE IF NOT EXISTS pokemon
        """

        # Execute the CREATE DATABASE statement
        executeMariaDB(cursor, createDatabaseQuery)

        # Commit the transaction
        commitMariaDB(conn)

        # Close cursor connection
        cursor.close()
        conn.close()

        print(f"Database pokemon created successfully.")
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error creating table: {e}")

# Function to create the table for sotring the pokemon
def createTableMariaDB(conn):
    try:
        cursor = conn.cursor()

        # Define the table name (replace 'your_table' with your preferred table name)
        tableName = 'pokemons'

        # Define the SQL CREATE TABLE statement
        createTableQuery = f"""
        CREATE TABLE IF NOT EXISTS {tableName} (
            Id VARCHAR(255) PRIMARY KEY,
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
        executeMariaDB(cursor, createTableQuery)

        # Commit the transaction
        commitMariaDB(conn)

        # Close cursor connection
        cursor.close()

        print(f"Table '{tableName}' created successfully.")
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error creating table: {e}")

# Function to retrieve column names from the database table
def getTableColumnsMariaDB(tableName, cursor):
    try:
        cursor.execute(f"DESCRIBE {tableName}")
        columns = [row[0] for row in cursor.fetchall()]
        return columns
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error describing table in MariaDB: {e}")
        return None

# Function to commit the changes made on a connection to MariaDB 
def commitMariaDB(conn):
    try: 
        conn.commit() 
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error commiting in MariaDB: {e}")

# Function to transform a JSON query into a SQL query
def jsonToSQL(data, tableName, columns):
    # Add backticks to column names
    escapedColumns = [f"`{column}`" for column in columns]
    # Construct the SQL INSERT statement
    insertQuery = f"INSERT INTO {tableName} ({', '.join(escapedColumns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    # Prepare the values from the JSON data
    values = [data.get(column) for column in columns]
    transform = {"insertQuery": insertQuery, "values": values}
    return transform

@app.route("/postPokemon", methods=['POST'] )
def postData():
    try:
        # Parse the JSON request data
        data = request.get_json()

        # Connect to the MariaDB database
        conn = connectMariaDB()
        cursor = conn.cursor()

        # Define the table to insert to
        tableName = 'pokemons'

        # Get the list of column names from the table schema
        columns = getTableColumnsMariaDB(tableName, cursor)

        # Transform from the http request to SQL query
        transform = jsonToSQL(data, tableName, columns)

        cursor.execute(transform["insertQuery"], transform["values"])
        commitMariaDB(conn)
        cursor.close()
        disconnectMariaDB(conn)

        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/deletePokemon/<id>", methods=['DELETE'] )
def deleteData(id):
    try:
        # Connect to the MariaDB database
        conn = connectMariaDB()
        cursor = conn.cursor()

        # Define the table to delete from
        tableName = "pokemons"

        # Construct the SQL DELETE statement
        deleteQuery = f"DELETE FROM {tableName} WHERE Id = %s"

        # Execute the SQL DELETE statement
        cursor.execute(deleteQuery, (id,))
        commitMariaDB(conn)
        cursor.close()
        disconnectMariaDB(conn)

        return jsonify({"message": "Data deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/putPokemon/<id>", methods=['PUT'] )
def putData(id):
    try:
        # Parse the JSON request data
        data = request.get_json()

        # Connect to the MariaDB database
        conn = connectMariaDB()
        cursor = conn.cursor()

        # Define the table to update
        tableName = 'pokemons'

        # Get the list of column names from the JSON request data
        columns = list(data.keys())

        # Construct the SQL UPDATE statement
        updateQuery = f"UPDATE {tableName} SET "
        updateQuery += ", ".join([f"{column} = %s" for column in columns])
        updateQuery += f" WHERE Id = {id}"  # Assuming 'Id' is the primary key

        # Prepare the values from the JSON data
        values = [data.get(column) for column in columns]

        # Execute the SQL UPDATE statement
        cursor.execute(updateQuery, values)
        commitMariaDB(conn)
        cursor.close()
        disconnectMariaDB(conn)

        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/getAllPokemon", methods=['GET'] )
def getAllData():
    try:
        # Connect to the MariaDB database
        conn = connectMariaDB()
        cursor = conn.cursor()

        # Define the table to query
        tableName = 'pokemons'

        # Get the list of column names from the table schema
        columns = getTableColumnsMariaDB(tableName, cursor)

        # Construct the SELECT query
        select_query = f"SELECT {', '.join(columns)} FROM {tableName}"

        cursor.execute(select_query)
        result = cursor.fetchall()

        cursor.close()
        disconnectMariaDB(conn)

        return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/getPokemon/<id>", methods=['GET'] )
def getData(id):
    try:
        # Connect to the MariaDB database
        conn = connectMariaDB()
        cursor = conn.cursor()

        # Define the table to query
        tableName = 'pokemons'

        # Get the list of column names from the table schema
        columns = getTableColumnsMariaDB(tableName, cursor)

        # Construct the SELECT query
        select_query = f"SELECT {', '.join(columns)} FROM {tableName} WHERE Id = %s"

        cursor.execute(select_query, (id,))
        result = cursor.fetchone()

        cursor.close()
        disconnectMariaDB(conn)

        if result:
            # Create a dictionary with column names as keys
            data_dict = dict(zip(columns, result))
            return jsonify(data_dict), 200
        else:
            return jsonify({"error": "Record not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Connect to the database and create the database anf table if it doesn´t exist, then disconnect
    conn = connectMariaDB()
    createDatabase()
    createTableMariaDB(conn)
    disconnectMariaDB(conn)

    # Run the Flask app
    app.run()
