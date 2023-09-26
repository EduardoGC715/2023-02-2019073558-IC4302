from flask import Flask, request, render_template_string
from flask_pymongo import PyMongo

app = Flask(__name__)

def mongoDBConnection (): 
    try:
        app.config["MONGO_URI"] = "mongodb+srv://eduardogc715:BasesII2023@bibliotec.6l341ym.mongodb.net/bibliotec"
        mongo = PyMongo(app)
        return mongo
    except Exception as e:
        print(f"An error occurred: {e}")