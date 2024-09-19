import uvicorn

from api import router
from core.config import settings
from utils.create_fastapi_app import create_app

app = create_app()

app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
        log_level=settings.run.log_level,
        workers=settings.run.workers,
    )
