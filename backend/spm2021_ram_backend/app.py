import time

import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from flask import Flask, Response
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_restful import Api

from spm2021_ram_backend.api.resources.convert_resource import ConvertApi

jwt = JWTManager()


def create_app(testing=False):
    """Application factory, used to create application"""

    app = Flask("bpmn_redrawer")
    CORS(app, origins=["*"])
    app.config.from_object("spm2021_ram_backend.config")

    if testing is True:
        app.config["TESTING"] = True

    jwt.init_app(app)
    add_resources(app)

    return app


def add_resources(app):
    """Add the routes to the Api of the given app"""

    api = Api(app)
    api.add_resource(ConvertApi, "/api/v1/convert")


AUTH = {"timer": 0, "cert": ""}


def get_public_keys(kid=None):
    """Get the public key in PEM format to validate the JWT token"""

    if time.time() - AUTH.get("timer") > 3600:
        response = requests.get(
            "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
            verify=True,
        )
        AUTH["cert"] = response.json()[kid]
        AUTH["timer"] = time.time()

    return AUTH.get("cert")


def convert_cert_to_pem(kid):
    """Get the certificate to validate the token in x509 format"""

    certificates = get_public_keys(kid)

    try:
        cert = x509.load_pem_x509_certificate(certificates.encode(), default_backend())
        rsa_public = cert.public_key()
    except Exception:
        return Response("Firebase Public Key error", 400)

    return rsa_public


@jwt.decode_key_loader
def decode_key_loader(claims, jwt_headers):
    return convert_cert_to_pem(claims.get("kid"))
