from flask import Flask
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    app.run()