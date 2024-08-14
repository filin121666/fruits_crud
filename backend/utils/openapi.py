from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.0.2",
        description=app.description,
        routes=app.routes,
    )
    
    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, method_item in path_item.items():
            if "responses" in method_item:
                responses = method_item["responses"]
                if "422" in responses:
                    del responses["422"]
    
    if "components" in openapi_schema:
        schemas = openapi_schema["components"].get("schemas", {})
        if "ValidationError" in schemas:
            del schemas["ValidationError"]
    
    return openapi_schema
