from flask import Flask
from app.views.index import Views

app = Flask(__name__)  # 初始化flask

@app.route("/", methods=["GET"])
def index():
    return Views.index()
