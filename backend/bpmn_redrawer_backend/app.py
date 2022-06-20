import sys
sys.path.append('.')
import os
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from bpmn_redrawer_backend.api.resources.convert_resource import convert_image
from bpmn_redrawer_backend.commons.utils import here


def create_app():
    debug = os.environ.get("BACKEND_MODE", "development").lower() == "development"
    app = Starlette(
        debug=debug,
        routes=[
            Route('/api/v1/convert', convert_image, methods=['POST']),
        ],
        middleware=[
            Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])
        ]
    )

    static_files_folder = here("static")
    if os.path.exists(static_files_folder) and os.path.isdir(static_files_folder):
        app.mount('/', StaticFiles(directory=static_files_folder, html=True))

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host='0.0.0.0', port=int(os.environ.get("BACKEND_PORT", "5000")))
