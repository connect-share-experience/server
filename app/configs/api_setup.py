"""This is where we configure all the API:
Title, include all routers, etc.
"""
from enum import Enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.configs.database_setup import create_db_and_tables
from app.configs.settings import StaticSettings
from app.routers import (authentication_router,
                         user_router,
                         friendship_router,
                         event_participant_router,
                         event_creator_router)


class Tags(Enum):
    """This enum class lists the API tags."""
    AUTH = "Authentication"
    USER = "User"
    FRIEND = "Friendship"
    EVENT_PART = "Event Participant"
    EVENT_CRE = "Event Creator"


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
    },
    {
        "name": Tags.EVENT_PART.value,
        "description": """Operations related to events and only accessible
                          to users that take part in that event."""
    },
    {
        "name": Tags.EVENT_CRE.value,
        "description": """Operations related to events and only accessible to
                          users that created that event."""
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
)  # TODO : allow only clients to access the API and learn about it


@app.on_event("startup")
def on_startup():
    """Actions to perform when starting the app."""
    create_db_and_tables()


# TODO : redundancies oin shutdown (save the data)

app.include_router(authentication_router.router, tags=[Tags.AUTH])
app.include_router(user_router.router, tags=[Tags.USER])
app.include_router(friendship_router.router, tags=[Tags.FRIEND])
# app.include_router(event_router.router, tags=[Tags.EVENT])
app.include_router(event_participant_router.router, tags=[Tags.EVENT_PART])
app.include_router(event_creator_router.router, tags=[Tags.EVENT_CRE])

app.mount("/user_page_picture",
          StaticFiles(directory=StaticSettings().user_page_pic_dir),
          name="user_page_picture")
app.mount("/event_page_picture",
          StaticFiles(directory=StaticSettings().event_page_pic_dir),
          name="event_page_picture")
app.mount("/event_pictures",
          StaticFiles(directory=StaticSettings().events_dir),
          name="event_pictures")
