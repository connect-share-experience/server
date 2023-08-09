"""API Runner."""
import uvicorn

# pylint: disable-next=unused-import
from app.configs.api_setup import app  # noqa: F401
from app.configs.settings import APISettings

settings = APISettings()

if __name__ == "__main__":
    uvicorn.run("app.main:app",
                host=settings.api_host,
                port=settings.api_port,
                reload=settings.api_reload)
