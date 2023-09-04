"""This module implements all the models used for the creation and the storage
of scores.

Classes
-------
Scores(SQLModel, table=True)
    Scores of users per category of events.
"""

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.users import User


class _ScoreBase(SQLModel):
    '''Base model for all score models.

    This contains the attributes that are common to each score model.
    For attributes and methods, see each specifics class.
    '''
    user_id: Optional[int]
    category_id: Optional[int]
    score: Optional[int]


class _ScoreBaseStrict(_ScoreBase):
    '''Similar to _ScoreBase, but with stricter restrictions.'''
    user_id: int
    category_id: int
    score: int


class ScoreCreate(_ScoreBaseStrict):
    '''Model for creating scores.

    Attributes
    ----------
    user_id: int
        id of the user.
    category_id: int
        id of the category.
    score: int
        score of the user in the category.
    '''


class ScoreUpdate(_ScoreBase):
    '''Model for updating scores.

    Attributes
    ----------
    user_id: Optional[int]
        id of the user.
    category_id: Optional[int]
        id of the category.
    score: Optional[int]
        score of the user in the category.
    '''


class ScoreRead(_ScoreBase):
    '''Model for reading scores.

    Attributes
    ----------
    user_id: Optional[int]
        id of the user.
    category_id: Optional[int]
        id of the category.
    score: Optional[int]
        score of the user in the category.
    '''


class Score(_ScoreBaseStrict, table=True):
    '''Model for reading scores.

    Attributes
    ----------
    user_id: int
        id of the user.
    category_id: int
        id of the category.
    score: int
        score of the user in the category.
    '''
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    category_id: int = Field(default=None, primary_key=True)
    score: int
    user: "User" = Relationship(back_populates="scores")
