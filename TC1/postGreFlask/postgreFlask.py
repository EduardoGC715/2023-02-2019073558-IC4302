from flask import Flask, redirect, url_for, render_template
import psycopg2
import os
import logging

app = Flask(__name__)

@app.route("/insert") #/home etc.
def insert():
    logger.debug("Received insert")
    return "Hello! this is the main page <h1>HELLO</h1>"
    #return render_template("index.html")

@app.route("/<name>") # grabs name value and passes it to function as a parameter.
def user(name):
    return render_template("index.html", content = name, r = 2, list = ["Tim", "Joe", "Bob"]) # content = name == variable inside html file.

@app.route("/admin")
def admin():
    return redirect(url_for("home")) # use the name of the function to redirect it to path.

@app.route("/admin1")
def admin1():
    return redirect(url_for("user", name="Admin!")) # use the name of the function to redirect it to path. To pass with parameters

def connect():
    postgre = None
    try:
        databasePG = os.getenv("PGDATABASE")
        username = os.getenv("PGUSER")
        passwordPG = os.getenv("PGPASSWORD")
        servicePG = os.getenv("PGSERVICE")
        logger.debug(databasePG)
        postgre = psycopg2.connect(
            host = servicePG,
            database= databasePG,
            user=username,
            password=passwordPG,
            port=5432
        )
        logger.debug("connected")
        cur = postgre.cursor()
        cur.execute('SELECT version()')
        logger.debug(cur.fetchone())

        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        logger.debug(error)
    finally:
        if postgre is not None:
            postgre.close()
            logger.debug('Database connection closed.')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    databasePG = os.getenv("PGDATABASE")
    username = os.getenv("PGUSER")
    passwordPG = os.getenv("PGPASSWORD")
    servicePG = os.getenv("PGSERVICE")
    logger.debug(databasePG)
   #connect()
    app.run()