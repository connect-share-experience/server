"""This module implements all the models used for the creation and the storage
of ranks.

Classes
-------
Ranks(SQLModel, table=True)
    Ranks of users per category of events.
"""

from typing import Optional
from sqlmodel import SQLModel  # , Field, Relationship


class _RankBase(SQLModel):
    '''Base model for all score models.

    This contains the attributes that are common to each score model.
    For attributes and methods, see each specifics class.
    '''
    user_id: Optional[int]
    category_id: Optional[int]
    score: Optional[int]


class _RankBaseStrict(_RankBase):
    '''Similar to _RankBase, but with stricter restrictions.'''
    user_id: int
    category_id: int
    score: int


class RankCreate(_RankBaseStrict):
    '''Model for creating ranks.

    Attributes
    ----------
    user_id: int
        id of the user.
    category_id: int
        id of the category.
    score: int
        score of the user in the category.
    '''


class RankUpdate(_RankBase):
    '''Model for updating ranks.

    Attributes
    ----------
    user_id: Optional[int]
        id of the user.
    category_id: Optional[int]
        id of the category.
    score: Optional[int]
        score of the user in the category.
    '''


class RankRead(_RankBase):
    '''Model for reading ranks.

    Attributes
    ----------
    user_id: Optional[int]
        id of the user.
    category_id: Optional[int]
        id of the category.
    score: Optional[int]
        score of the user in the category.
    '''


class Score(_RankBaseStrict, table=True):
    '''Model for reading ranks.

    Attributes
    ----------
    user_id: int
        id of the user.
    category_id: int
        id of the category.
    score: int
        score of the user in the category.
    '''
