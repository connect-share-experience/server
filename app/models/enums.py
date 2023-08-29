"""This module implements enum classes used in models.

These classes are used as attributes, and allow for better control of values
passed into those attributes.

Classes
-------
UserEventStatus
    Possible status for User-Event relationship.
EventCategory
    Possible types of events.
MessageCategory
    Possible types of messages.
InteractionCatergory
    Possible types of interactions.
"""

from enum import Enum


class _StrEnum(str, Enum):
    """This class is a base for all str enums.

    It allows for attributes that are an enum to be printed directly as strings
    when printed within a class.
    """
    def __repr__(self) -> str:
        return str.__repr__(self.value)


class UserEventStatus(_StrEnum):
    """This Enum class lists the different possible status for User-Event."""
    ATTENDS = "attends"
    CREATOR = "creator"
    DELETED = "deleted"
    DENIED = "denied"
    PENDING = "pending"


class EventCategory(_StrEnum):
    """This Enum class lists the different possible types of events."""
    PARTY = "party"
    SPORTS = "sports"
    CULTURE = "culture"
    MOVIES = "movies"
    GAMING = "gaming"
    OTHER = "other"


class MessageCategory(_StrEnum):
    """This Enum class lists the different possible types of messages."""
    ORGA = "orga"
    ADDED = "added"
    DELETED = "deleted"
    PICTURE = "picture"


class InteractionCatergory(_StrEnum):
    """This Enum class lists the different possible types of interactions."""
    FR_SEND = "friend_request_send"
    FR_ACCEPTED = "friend_request_accepted"
    FR_REFUSED = "friend_request_refused"
    FR_IGNORED = "friend_request_ignored"
    NO_INTERACTION = "no_interaction"
    USER_REPORT = "user_report"
    USER_REPORTED = "user_reported"
    EVENT_POSITIVE = "positive_event"
    EVENT_NEGATIVE = "negative_event"
