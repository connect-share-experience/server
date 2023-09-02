"""This module implements classes to handle database access for ranking
information.

Classes
-------
RankingInfoDao(session)
    Data access for ranking information.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.ranking_info import RankingInfo, RankingInfoUpdate
from app.models.enums import EventCategory


class RankingInfoDao:
    """Data Access for ranking information.

    This class implements all methods for database operations for ranking
    information.
    All methods return a RankingInfo object.

    Methods
    -------
    create_ranking_info(self, ranking_info)
        Add new ranking information in the database.
    read_ranking_info(self, category)
        Read ranking information from the database using its category.
    read_ranking_infos(self, offset, limit)
        Read ranking information from the database between offset and
        offset+limit.
    update_ranking_info(self, category, new_info)
        Update ranking information in the database with new data.
    delete_ranking_info(self, category)
        Delete ranking information from the database using its category.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_ranking_info(self, ranking_info: RankingInfo) -> RankingInfo:
        """Create new ranking information in the DB.

        Parameters
        ----------
        ranking_info : RankingInfo
            The ranking information to add to the database.

        Returns
        -------
        RankingInfo
            The created ranking information.
        """
        self.session.add(ranking_info)
        self.session.commit()
        self.session.refresh(ranking_info)
        return ranking_info

    def read_ranking_info(self, category: EventCategory) -> RankingInfo:
        """Read a single ranking information using its category.

        Parameters
        ----------
        category : EventCategory
            The category of the ranking information to read.

        Returns
        -------
        RankingInfo
            The ranking information that was read.

        Raises
        ------
        HTTPException
            Raised when there is no ranking information with that category.
        """
        statement = select(RankingInfo).where(RankingInfo.category == category)
        ranking_info = self.session.exec(statement).one_or_none()
        if ranking_info is None:
            raise HTTPException(status_code=404,
                                detail="Ranking information for category" +
                                f"{category} not found.")
        return ranking_info

    def read_ranking_infos(self, offset: int, limit: int) -> List[RankingInfo]:
        """Read all ranking information from offset to offset+limit in the
        table.

        Parameters
        ----------
        offset : int
            Index at which to start reading.
        limit : int
            Number of entries to read.

        Returns
        -------
        List[RankingInfo]
            The ranking information read from the table.
        """
        statement = select(RankingInfo).offset(offset).limit(limit)
        ranking_infos = self.session.exec(statement).all()
        return ranking_infos

    def update_ranking_info(self,
                            category: EventCategory,
                            new_info: RankingInfoUpdate) -> RankingInfo:
        """Update ranking information for a specific category.

        Parameters
        ----------
        category : EventCategory
            The category of the ranking information to update.
        new_info : RankingInfoUpdate
            The new ranking information to use for the update.

        Returns
        -------
        RankingInfo
            The updated ranking information.

        Raises
        ------
        HTTPException
            Raised when there is no ranking information for that category.
        """
        old_ranking_info = self.read_ranking_info(category)
        new_data = new_info.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_ranking_info, key, value)

        self.session.add(old_ranking_info)
        self.session.commit()
        self.session.refresh(old_ranking_info)
        return old_ranking_info

    def delete_ranking_info(self, category: EventCategory) -> RankingInfo:
        """Delete ranking information for a specific category.

        Parameters
        ----------
        category : EventCategory
            The category of the ranking information to delete.

        Returns
        -------
        RankingInfo
            The deleted ranking information.

        Raises
        ------
        HTTPException
            Raised when there is no ranking information for that category.
        """
        ranking_info = self.read_ranking_info(category)
        if not ranking_info:
            raise HTTPException(status_code=404,
                                detail="Ranking information for category" +
                                f"{category} not found.")
        self.session.delete(ranking_info)
        self.session.commit()
        return ranking_info
