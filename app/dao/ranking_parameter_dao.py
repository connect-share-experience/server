"""This module implements classes to handle database access for ranking
parameters.

Classes
-------
RankingParameterDao(session)
    Data access for ranking parameters.
"""

from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.ranking_parameters import (
    RankingParameters,
    RankingParametersCreate,
    RankingParametersUpdate,
)
from app.models.enums import EventCategory


class RankingParameterDao:
    """Data Access for ranking parameters.

    This class implements all methods for database operations for ranking
    parameters.
    All methods return a RankingParameters object or a list of
    RankingParameters objects.

    Methods
    -------
    create_ranking_parameter(ranking_parameter)
        Add a new ranking parameter in the database.
    read_ranking_parameter(user_id, event_id, category)
        Read a ranking parameter from the database using user_id,
        event_id, and category.
    read_ranking_parameter_per_user(user_id)
        Read all ranking parameters for a specific user.
    read_ranking_parameter_per_category(category)
        Read all ranking parameters for a specific category.
    read_ranking_parameter_per_event(event_id)
        Read all ranking parameters for a specific event.
    read_ranking_parameters(offset, limit)
        Read ranking parameters from the database between offset and
        offset+limit.
    update_ranking_parameter(user_id,
                            event_id,
                            category,
                            new_ranking_parameter)
        Update a ranking parameter in the database.
    delete_ranking_parameter(user_id, event_id, category)
        Delete a ranking parameter from the database.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_ranking_parameter(
         self,
         ranking_parameter: RankingParametersCreate) -> RankingParameters:
        """Create a new RankingParameters entry in the database.

        Parameters
        ----------
        ranking_parameter : RankingParametersCreate
            The ranking parameter to add to the database.

        Returns
        -------
        RankingParameters
            The created ranking parameter.
        """
        self.session.add(ranking_parameter)
        self.session.commit()
        self.session.refresh(ranking_parameter)
        return ranking_parameter

    def read_ranking_parameter(
         self,
         user_id: int,
         event_id: int,
         category: EventCategory) -> Optional[RankingParameters]:
        """Read a ranking parameter using user_id, event_id, and category.

        Parameters
        ----------
        user_id : int
            The user ID.
        event_id : int
            The event ID.
        category : EventCategory
            The event category.

        Returns
        -------
        Optional[RankingParameters]
            The ranking parameter that was read, or None if not found.

        Raises
        ------
        HTTPException
            Raised when there is no ranking parameter with the given
            identifiers.
        """
        statement = (
            select(RankingParameters)
            .where(
                (RankingParameters.user_id == user_id)
                & (RankingParameters.event_id == event_id)
                & (RankingParameters.category == category)
            )
        )
        ranking_parameter = self.session.exec(statement).one_or_none()
        if ranking_parameter is None:
            raise HTTPException(status_code=404, detail="Ranking parameter" +
                                " not found.")
        return ranking_parameter

    def read_ranking_parameter_per_user(
         self,
         user_id: int) -> List[RankingParameters]:
        """Read all ranking parameters for a specific user.

        Parameters
        ----------
        user_id : int
            The user ID.

        Returns
        -------
        List[RankingParameters]
            The ranking parameters for the specified user.
        """
        statement = select(RankingParameters).where(
            RankingParameters.user_id == user_id)
        ranking_parameters = self.session.exec(statement).all()
        return ranking_parameters

    def read_ranking_parameter_per_category(
         self,
         category: EventCategory) -> List[RankingParameters]:
        """Read all ranking parameters for a specific category.

        Parameters
        ----------
        category : EventCategory
            The event category.

        Returns
        -------
        List[RankingParameters]
            The ranking parameters for the specified category.
        """
        statement = select(
            RankingParameters).where(
                RankingParameters.category == category)
        ranking_parameters = self.session.exec(statement).all()
        return ranking_parameters

    def read_ranking_parameter_per_event(
         self,
         event_id: int) -> List[RankingParameters]:
        """Read all ranking parameters for a specific event.

        Parameters
        ----------
        event_id : int
            The event ID.

        Returns
        -------
        List[RankingParameters]
            The ranking parameters for the specified event.
        """
        statement = select(RankingParameters).where(
            RankingParameters.event_id == event_id)
        ranking_parameters = self.session.exec(statement).all()
        return ranking_parameters

    def read_ranking_parameters(self,
                                offset: int,
                                limit: int) -> List[RankingParameters]:
        """Read ranking parameters from the database between offset and
        offset+limit.

        Parameters
        ----------
        offset : int
            The offset index.
        limit : int
            The limit for the number of records to retrieve.

        Returns
        -------
        List[RankingParameters]
            The ranking parameters within the specified range.
        """
        statement = select(RankingParameters).offset(offset).limit(limit)
        ranking_parameters = self.session.exec(statement).all()
        return ranking_parameters

    def update_ranking_parameter(
         self,
         user_id: int,
         event_id: int,
         category: EventCategory,
         new_ranking_parameter: RankingParametersUpdate) -> RankingParameters:
        """Update a ranking parameter in the database.

        Parameters
        ----------
        user_id : int
            The user ID.
        event_id : int
            The event ID.
        category : EventCategory
            The event category.
        new_ranking_parameter : RankingParametersUpdate
            The new ranking parameter data.

        Returns
        -------
        RankingParameters
            The updated ranking parameter.

        Raises
        ------
        HTTPException
            Raised when there is no ranking parameter with the given
            identifiers.
        """
        old_ranking_parameter = self.read_ranking_parameter(user_id,
                                                            event_id,
                                                            category)
        if old_ranking_parameter is None:
            raise HTTPException(status_code=404,
                                detail="Ranking parameter not found.")

        new_data = new_ranking_parameter.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_ranking_parameter, key, value)

        self.session.add(old_ranking_parameter)
        self.session.commit()
        self.session.refresh(old_ranking_parameter)
        return old_ranking_parameter

    def delete_ranking_parameter(self,
                                 user_id: int,
                                 event_id: int,
                                 category: EventCategory) -> RankingParameters:
        """Delete a ranking parameter from the database.

        Parameters
        ----------
        user_id : int
            The user ID.
        event_id : int
            The event ID.
        category : EventCategory
            The event category.

        Returns
        -------
        RankingParameters
            The deleted ranking parameter.

        Raises
        ------
        HTTPException
            Raised when there is no ranking parameter with the given
            identifiers.
        """
        ranking_parameter = self.read_ranking_parameter(user_id,
                                                        event_id,
                                                        category)
        if ranking_parameter is None:
            raise HTTPException(status_code=404,
                                detail="Ranking parameter not found.")

        self.session.delete(ranking_parameter)
        self.session.commit()
        return ranking_parameter
