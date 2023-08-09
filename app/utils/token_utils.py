"""Functions related to authentication by token"""
from typing import Any, Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.configs.settings import AuthSettings

SECRET_KEY = AuthSettings().key
ALGORITHM = AuthSettings().algo


def create_access_token(data: dict[str, Any],
                        expires_delta: Optional[timedelta] = None) -> str:
    """Create proper tokens for authentication.

    Parameters
    ----------
    data : dict[str, Any]
        Data to encode in the token.
    expires_delta : Optional[timedelta], optional
        The time before the token exprires, in minutes, by default None

    Returns
    -------
    str
        The token

    Raises
    ------
    JWTError
        Raised when jwt failed to encore the token as a str.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if not isinstance(encoded_jwt, str):
        raise JWTError
    return encoded_jwt
