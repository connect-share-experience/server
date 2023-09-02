"""This module implements classes to handle database access for scores.

Classes
-------
ScoreDao(session)
    Data access for scores.
"""
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.scores import Score, ScoreUpdate


class ScoreDao:
    """Data Access for scores.

    This class implements all methods for database operations for scores.
    All methods return a Score object.

    Methods
    -------
    create_score(self, score)
        Add a new score in database.
    read_score(self, score_id)
        Read a score from database using its id.
    read_scores(self, offset, limit)
        Read scores from database between offset and offset+limit.
    update_score(self, score_id, new_score)
        Update a score in database with new score data.
    delete_score(self, score_id)
        Delete a score from database using its id.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_score(self, score: Score) -> Score:
        """Create a new Score in DB.

        Parameters
        ----------
        score : Score
            The score to add to database.

        Returns
        -------
        Score
            The created score.
        """
        self.session.add(score)
        self.session.commit()
        self.session.refresh(score)
        return score

    def read_score(self, score_id: int) -> Score:
        """Read a single score using its id.

        Parameters
        ----------
        score_id : int
            The id of the score to read.

        Returns
        -------
        Score
            The score that was read.

        Raises
        ------
        HTTPException
            Raised when there is no score with that id.
        """
        score = self.session.get(Score, score_id)
        if score is None:
            raise HTTPException(status_code=404,
                                detail=f"Score with id {score_id} not found.")
        return score

    def read_scores(self, offset: int, limit: int) -> List[Score]:
        """Read all scores from offset to offset+limit in the table.

        Parameters
        ----------
        offset : int
            Index at which to start reading.
        limit : int
            Number of entries to read.

        Returns
        -------
        List[Score]
            The scores read from table.
        """
        statement = select(Score).offset(offset).limit(limit)
        scores = self.session.exec(statement).all()
        return scores

    def update_score(self, score_id: int, new_score: ScoreUpdate) -> Score:
        """Update a score with chosen id with new score data.

        Parameters
        ----------
        score_id : int
            id of the score to update.
        new_score : ScoreUpdate
            The new score whose data to use for the update.

        Returns
        -------
        Score
            The updated score.

        Raises
        ------
        HTTPException
            Raised when there is no score with that id.
        """
        old_score = self.session.get(Score, score_id)
        if not old_score:
            raise HTTPException(status_code=404,
                                detail=f"Score with id {score_id} not found.")
        new_data = new_score.dict(exclude_unset=True)
        for key, value in new_data.items():
            setattr(old_score, key, value)

        self.session.add(old_score)
        self.session.commit()
        self.session.refresh(old_score)
        return old_score

    def delete_score(self, score_id: int) -> Score:
        """Delete a score using its id.

        Parameters
        ----------
        score_id : int
            The id of the score to delete.

        Returns
        -------
        Score
            The deleted score.

        Raises
        ------
        HTTPException
            Raised when there is no score with that id.
        """
        score = self.session.get(Score, score_id)
        if not score:
            raise HTTPException(status_code=404,
                                detail=f"Score with id {score_id} not found.")
        self.session.delete(score)
        self.session.commit()
        return score
