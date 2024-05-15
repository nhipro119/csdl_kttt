from flask import request, Flask, Response, send_from_directory
import json
import os
from werkzeug.utils import secure_filename
from application.application import Application
class Api:
    def __init__(self):
        self.app = Application
    def search(self):
        if request.method =="POST":
            pass

    def ping(self):
        if request.method == "GET":
            return Response(json.dumps({"ping":"success"}), status=200, mimetype="application/json")