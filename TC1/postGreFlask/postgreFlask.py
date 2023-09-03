from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/insert") #/home etc.
def insert():
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




if __name__ == "__main__":
    app.run()