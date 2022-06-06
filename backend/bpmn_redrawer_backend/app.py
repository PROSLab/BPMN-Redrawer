from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from bpmn_redrawer_backend.api.resources.convert_resource import ConvertApi


def create_app(testing=False):
    """Application factory, used to create application"""

    app = Flask("bpmn_redrawer")
    CORS(app, origins=["*"])
    app.config.from_object("bpmn_redrawer_backend.config")

    if testing is True:
        app.config["TESTING"] = True

    add_resources(app)

    return app


def add_resources(app):
    """Add the routes to the Api of the given app"""

    api = Api(app)
    api.add_resource(ConvertApi, "/api/v1/convert")
