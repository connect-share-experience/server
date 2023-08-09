"""This is where we configure all the API:
Title, include all routers, etc.
"""
from enum import Enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs.database_setup import create_db_and_tables
from app.routers import (authentication_router,
                         user_router,
                         friendship_router)


class Tags(Enum):
    """This enum class lists the API tags."""
    AUTH = "Authentication"
    USER = "User"
    FRIEND = "Friendship"


tags_metadata = [
    {
        "name": Tags.AUTH.value,
        "description": "Operations related to register/login."
    },
    {
        "name": Tags.USER.value,
        "description": "Operations related to user information."
    },
    {
        "name": Tags.FRIEND.value,
        "description": """Operations related to friendship creation,
                          modification and deletion."""
    }
]


app = FastAPI(
    title="Connect",
    version="0.0.1",
    description="Share moments",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event("startup")
def on_startup():
    """Actions to perform when starting the app."""
    create_db_and_tables()


app.include_router(authentication_router.router, tags=[Tags.AUTH])
app.include_router(user_router.router, tags=[Tags.USER])
app.include_router(friendship_router.router, tags=[Tags.FRIEND])
