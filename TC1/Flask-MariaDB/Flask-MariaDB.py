import mariadb
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to connect to MariaDB
def connectMariaDB():
    try:
        conn = mariadb.connect(
            # TODO: Update to use environment variables or secrets
            user="root",
            password="uwJKdwvjY2",
            host="localhost",
            database="pokemon",
            port= "59236"
        )
        return conn
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error connecting to MariaDB: {e}")
        return None


def disconnectMariaDB(conn):
    try:
        conn.close()
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error closing MariaDB connection: {e}")

def executeMariaDB(cursor, query):
    try:
        cursor.execute(query)
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error executing MariaDB query: {e}")

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
            `Type 1` VARCHAR(255),
            `Type 2` VARCHAR(255),
            Category VARCHAR(255),
            `Height (ft)` VARCHAR(255),
            `Height (m)` VARCHAR(255),
            `Weight (lbs)` VARCHAR(255),
            `Weight (kg)` VARCHAR(255),
            `Capture Rate` VARCHAR(255),
            `Egg Steps` VARCHAR(255),
            `Exp Group` VARCHAR(255),
            Total VARCHAR(255),
            HP VARCHAR(255),
            Attack VARCHAR(255),
            Defense VARCHAR(255),
            `Sp Attack` VARCHAR(255),
            `Sp Defense` VARCHAR(255),
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
    
def commitMariaDB(conn):
    try: 
        conn.commit() 
    except mariadb.Error as e:
        # Handle the exception
        print(f"Error commiting in MariaDB: {e}")

@app.route("/mariadb/pokemon", methods=['POST'] )
def postData():
    try:
        # Parse the JSON request data
        data = request.get_json()

        # Connect to the MariaDB database
        conn = connectMariaDB()
        cursor = conn.cursor()

        # Construct the SQL INSERT statement based on the JSON data
        tableName = 'pokemons'

        # Get the list of column names from the table schema
        columns = getTableColumnsMariaDB(tableName)

        # Construct the SQL INSERT statement
        insert_query = f"INSERT INTO {tableName} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

        # Prepare the values from the JSON data
        values = [data.get(column) for column in columns]

        cursor.execute(insert_query, values)
        commitMariaDB(conn)
        cursor.close()
        disconnectMariaDB(conn)

        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mariadb/pokemon/<pokemonID>", methods=['DELETE'] )
def deleteData():
    return "<p>Hello, World!</p>"

@app.route("/mariadb/pokemon", methods=['PUT'] )
def putData():
    return "<p>Hello, World!</p>"

@app.route("/mariadb/pokemon/<pokemonID>", methods=['GET'] )
def getData():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    conn = connectMariaDB()
    createTableMariaDB(conn)
    app.run()
