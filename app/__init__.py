from flask import Flask


app = Flask(__name__)  # 初始化flask
app.config.from_object("config")

