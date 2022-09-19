from app import app

from flask import Flask
from app.views.index import Views

@app.route("/", methods=["GET"])
def index():
    return Views.index()
