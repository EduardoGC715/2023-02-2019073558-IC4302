from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content = name)

@app.route("/mysql/get", methods=["POST", "GET"])
def user(name):
    return f"Hello {name}!"


@app.route("/mondodb/get", methods=["POST", "GET"]) 
def admin():
    return redirect(url_for("user", name = "Admin!"))


if __name__ == "__main__":
    app.run()