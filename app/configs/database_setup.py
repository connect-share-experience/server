"""This module implements all steps to setup the software.

Functions
---------
create_db_and_tables() -> None
    Create database and table.
delete_db()
    Delete database.
"""
# pylint: disable=unused-import

import os

from sqlmodel import SQLModel, create_engine

from app.configs.settings import DBSettings
from app.models.addresses import Address  # noqa: F401
from app.models.events import Event  # noqa: F401
from app.models.latitudes_longitudes import LatLon  # noqa: F401
from app.models.links import Friendship, UserEventLink  # noqa: F401
from app.models.messages import Message  # noqa: F401
from app.models.ranking_info import RankingInfo  # noqa: F401
from app.models.ranking_parameters import RankingParameters  # noqa: F401
from app.models.scores import Score  # noqa: F401
from app.models.users import User  # noqa: F401


settings = DBSettings()

engine = create_engine(
    settings.url,
    echo=settings.echo,
    connect_args={"check_same_thread": settings.thread}
)


def create_db_and_tables() -> None:
    """Create database with all tables."""
    SQLModel.metadata.create_all(engine)


def delete_db() -> None:
    """Delete database."""
    os.remove(settings.path)
