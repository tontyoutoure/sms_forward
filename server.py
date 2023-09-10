from flask import Flask
import utils
from flask import request
import json

json_file = open("bot_info.json", "r")
bot_info = json.load(json_file)
json_file.close()

app = Flask(__name__)

print("server started")

@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "GET":
        return "<p>Hello, World!</p>"
    else:
        data = request.get_data()
        form = request.form.to_dict()
        print(data)
        print(form)
        return "received"