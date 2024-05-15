import flask
from Config.reader import Reader
import json
from delivery.handle import Handle
from flask_cors import CORS, cross_origin

server_config = Reader()
config = server_config.get_service_config()

app = flask.Flask(config["SERVER"]["NAME"])
cors = CORS(app)

app.config["CORS_HEADER"] = "Content-Type"

app = Handle().setup(app)

if __name__ == "__main__":
    
    app.run(host=config["SERVER"]["HOST"], port=config["SERVER"]["PORT"], debug = False, threaded=False)