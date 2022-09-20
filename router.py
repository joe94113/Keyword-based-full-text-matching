from app import app

from flask import Flask
from app.views.index import Views
from app.views.search import Search

@app.route("/test", methods=["GET"])
def test():
    return Views.index()

@app.route("/", methods=["GET"])
def index():
    return Search.index()
