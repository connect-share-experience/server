"""This module implements all the models used for the creation and the storage
of ranking information.

Classes
-------
RankingInfo(SQLModel, table=True)
    Percentile information for each category of events.
"""

from typing import Optional
from sqlmodel import SQLModel, Field
from app.models.enums import EventCategory


class _RankingInfoBase(SQLModel):
    '''Base model for all ranking information models.

    This contains the attributes that are common to each ranking information
    model.

    For attributes and methods, see each specific class.
    '''

    category: Optional[EventCategory]
    p20: Optional[float]
    p40: Optional[float]
    p60: Optional[float]
    p80: Optional[float]
    median: Optional[float]


class _RankingInfoBaseStrict(_RankingInfoBase):
    '''Similar to _RankingInfoBase, but with stricter restrictions.'''
    category: EventCategory
    p20: float
    p40: float
    p60: float
    p80: float
    median: float


class RankingInfoCreate(_RankingInfoBaseStrict):
    '''Model for creating ranking information.

    Attributes
    ----------
    category: EventCategory
        Category of the event.
    p20: float
        20th percentile score.
    p40: float
        40th percentile score.
    p60: float
        60th percentile score.
    p80: float
        80th percentile score.
    median: float
        Median score.
    '''


class RankingInfoUpdate(_RankingInfoBase):
    '''Model for updating ranking information.

    Attributes
    ----------
    category: Optional[EventCategory]
        Category of the event.
    p20: Optional[float]
        20th percentile score.
    p40: Optional[float]
        40th percentile score.
    p60: Optional[float]
        60th percentile score.
    p80: Optional[float]
        80th percentile score.
    median: Optional[float]
        Median score.
    '''


class RankingInfoRead(_RankingInfoBase):
    '''Model for reading ranking information.

    Attributes
    ----------
    category: Optional[EventCategory]
        Category of the event.
    p20: Optional[float]
        20th percentile score.
    p40: Optional[float]
        40th percentile score.
    p60: Optional[float]
        60th percentile score.
    p80: Optional[float]
        80th percentile score.
    median: Optional[float]
        Median score.
    '''


class RankingInfo(_RankingInfoBaseStrict, table=True):
    '''Model for storing ranking information in the database.

    Attributes
    ----------
    category: EventCategory
        Category of the event.
    p20: float
        20th percentile score.
    p40: float
        40th percentile score.
    p60: float
        60th percentile score.
    p80: float
        80th percentile score.
    median: float
        Median score.
    '''
    category: EventCategory = Field(default=None, primary_key=True)
    p20: float
    p40: float
    p60: float
    p80: float
    median: float
