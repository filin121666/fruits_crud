from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from core.database import database
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from core.config import settings
from fastapi.middleware.gzip import GZipMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await database.dispose()


def register_custom_doc_urls(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.cdn.swagger_js_url,
            swagger_css_url=settings.cdn.swagger_css_url,
            swagger_ui_parameters={"operationsSorter": "method"},
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=settings.cdn.redoc_js_url,
        )


def create_app() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        title=settings.api.title,
        description=settings.api.description,
        version=settings.api.version,
        debug=False,
        docs_url=None if settings.api.create_custom_doc_urls else "/docs",
        redoc_url=None if settings.api.create_custom_doc_urls else "/redoc",
    )
    
    if settings.api.create_custom_doc_urls:
        register_custom_doc_urls(app=app)

    if settings.api.use_gzip:
        app.add_middleware(
            GZipMiddleware,
            minimum_size=1500,
            compresslevel=6,
        )

    return app
