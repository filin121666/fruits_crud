from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router
from core.config import settings
from core.database import database
from utils.openapi import custom_openapi


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await database.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    title="Fruits CRUD",
    description="Is an application that implements CRUD (create, read, update, delete) operations on fruits",
    version="1.0",
    debug=False,
)

app.openapi = lambda: custom_openapi(app=app)
app.include_router(
    router=router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        # reload=True,  # Если разработка то разкоментировать
        log_level="error",  # если разработка, то поменять на log_level="info"
    )
