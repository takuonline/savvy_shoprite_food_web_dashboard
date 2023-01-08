from flask import render_template
from flask import current_app as app

version = "0.1.0"

@app.route("/version")
def home():
    return  f"<h1> version {version}/h1>"



