"""This module implements all the models used for the creation and the storage
of ranking parameters.

Classes
-------
RankingParameters(SQLModel, table=True)
    Ranking parameters for each user for each round (event) and each category.
"""

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.enums import EventCategory
from app.models.users import User
from app.models.events import Event


class _RankingParametersBase(SQLModel):
    '''Base model for all ranking parameters models.

    This contains the attributes that are common to each ranking parameters
    model.

    For attributes and methods, see each specific class.
    '''
    user_id: Optional[int]
    event_id: Optional[int]
    category: Optional[EventCategory]
    p: Optional[float]
    w: Optional[float]


class _RankingParametersBaseStrict(_RankingParametersBase):
    '''Similar to _RankingParametersBase, but with stricter restrictions.'''
    user_id: int
    event_id: int
    category: EventCategory
    p: float
    w: float


class RankingParametersCreate(_RankingParametersBaseStrict):
    '''Model for creating ranking parameters.'''


class RankingParametersUpdate(_RankingParametersBase):
    '''Model for updating ranking parameters.'''


class RankingParametersRead(_RankingParametersBase):
    '''Model for reading ranking parameters.'''


class RankingParameters(_RankingParametersBaseStrict, table=True):
    '''Model for storing ranking parameters in the database.'''
    user_id: int = Field(default=None,
                         primary_key=True,
                         foreign_key="user.id")
    event_id: int = Field(default=None,
                          primary_key=True,
                          foreign_key="event.id")
    category: EventCategory = Field(default=None, primary_key=True)
    p: float
    w: float

    # Relationships
    user: "User" = Relationship(back_populates="ranking_parameters")
    event: "Event" = Relationship(back_populates="ranking_parameters")
