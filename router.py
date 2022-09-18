from app import app
from app.views.index import Views


@app.route("/", methods=["GET"])
def index():
    return Views.index()
