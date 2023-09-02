"""This module defines all models used to handle users.

These classes collect all data related to the app users, from their name and
contact info to their friends list.

Classes
-------
UserCreate(SQLModel)
    Model for creating users.
UserUpdate(SQLModel)
    Model for creating users.
UserRead(SQLModel)
    Model for reading users.
User(SQLModel, table=True)
    Model for users in database.
"""
from datetime import date
from typing import List, Optional, TYPE_CHECKING

from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.models.messages import Message
from app.models.scores import Score
from app.models.ranking_parameters import RankingParameters
from app.utils.regex_utils import CITY_REGEX, NAME_REGEX
from app.utils.validators import check_valid_phone
if TYPE_CHECKING:
    from app.models.links import UserEventLink, Friendship


class _UserBase(SQLModel):
    """Base model for all user models.

    This contains the attributes that are common to each user model.
    For attributes and methods, see each specific class.
    """
    phone: Optional[str]
    first_name: Optional[str] = Field(max_length=20, regex=NAME_REGEX)
    last_name: Optional[str] = Field(max_length=40, regex=NAME_REGEX)
    bio: Optional[str] = Field(max_length=500)
    city: Optional[str] = Field(max_length=50, regex=CITY_REGEX)

    @classmethod
    @validator("phone")
    def phone_validator(cls, value: str) -> str:
        """Verify that the input value is a valid phone number.

        Parameters
        ----------
        value : str
            The input value to check.

        Returns
        -------
        str
            The string representing a phone number.
        """
        return check_valid_phone(value)


class _UserBaseStrict(_UserBase):
    """Similar to _UserBase, but with stricter restrictions."""
    first_name: str = Field(max_length=20, regex=NAME_REGEX)
    last_name: str = Field(max_length=40, regex=NAME_REGEX)
    phone: str


class UserUpdate(_UserBase):
    """Model for updating users.

    Attributes
    ----------
    first_name: Optional[str]
        First name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    last_name: Optional[str]
        Last name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    phone: Optional[str]
        Phone number of the user. Has validation with check_valid_phone().
    bio: Optional[str]
        Description of the user. Maximum 500 characters.
    city: Optional[str]
        Main city of the user. Specific regex validation.

    Methods
    -------
    check_valid_phone(cls, value: str) : validator("phone")
        Validates that the value is a valid phone number.
    """


class UserCreate(_UserBaseStrict):
    """Model for creating users.

    Attributes
    ----------
    first_name: str
        First name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    last_name: str
        Last name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    phone: str
        Phone number of the user. Has validation with check_valid_phone().
    bio: Optional[str]
        Description of the user. Maximum 500 characters.
    city: Optional[str]
        Main city of the user. Specific regex validation.

    Methods
    -------
    check_valid_phone(cls, value: str) : validator("phone")
        Validates that the value is a valid phone number.
    """


class UserRead(_UserBaseStrict):
    """Model for reading users.

    Attributes
    ----------
    first_name: str
        First name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    last_name: str
        Last name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    phone: str
        Phone number of the user. Has validation with check_valid_phone().
    bio: Optional[str]
        Description of the user. Maximum 500 characters.
    city: Optional[str]
        Main city of the user. Specific regex validation.
    score: int
        ELO score of the user in the app.
    register_date: datetime.date
        The date at which the user registered.
    id: int
        Unique user identifier.

    Methods
    -------
    check_valid_phone(cls, value: str) : validator("phone")
        Validates that the value is a valid phone number.
    """
    id: int
    score: int
    register_date: date
    picture: str


class User(_UserBaseStrict, table=True):
    """Model for users in database.

    Attributes
    ----------
    first_name: str
        First name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    last_name: str
        Last name of the user.
        Must be maximum 20 characters, and has specific regex validation.
    phone: str
        Phone number of the user. Has validation with check_valid_phone().
        Has a unique constraint.
    bio: Optional[str]
        Description of the user. Maximum 500 characters.
    city: Optional[str]
        Main city of the user. Specific regex validation.
    score: int
        ELO score of the user in the app. Defaults to 1000.
    register_date: datetime.date
        The date at which the user registered.
    id: Optional[int]
        Unique user identifier. Filled upon creation in database.
    event_links: List[UserEventLinks]
        The links betwenn the user and the events he created, requested,
        attended, was denied from, etc.
    sent_invites: List[Friendship]
        The friendship requested by the user, i.e they sent the invite.

    Methods
    -------
    check_valid_phone(cls, value: str) : validator("phone")
        Validates that the value is a valid phone number.
    """
    __table_args__ = (UniqueConstraint("phone"),)

    id: int = Field(default=None, primary_key=True)
    register_date: date = Field(default=date.today())
    score: Optional[int] = Field(default=1000)
    picture: str = Field(default="default_user_pic.png")

    messages: List["Message"] = Relationship(back_populates="user")
    event_links: List["UserEventLink"] = Relationship(back_populates="user")
    sent_invites: List["Friendship"] = Relationship(
        back_populates="invite_sender",
        sa_relationship_kwargs={
            "foreign_keys": "Friendship.invite_sender_id"})
    received_invites: List["Friendship"] = Relationship(
        back_populates="invite_receiver",
        sa_relationship_kwargs={
            "foreign_keys": "Friendship.invite_receiver_id"})
    scores: List["Score"] = Relationship(back_populates="user")
    ranking_parameters: List["RankingParameters"] = Relationship(
                                                        back_populates="user")