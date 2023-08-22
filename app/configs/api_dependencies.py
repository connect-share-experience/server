"""This modules contains functions used as dependencies through the API.

Functions
---------
get_session()
    Yield a database session for the app.
get_current_admin()
    Return the admin currently authenticated.
"""
from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt
from sqlmodel import Session

from app.configs.database_setup import engine
from app.configs.settings import AuthSettings
from app.models.tokens import TokenData
from app.models.users import User
from app.services.user_services import UserService


def get_session():
    """Yield session for the whole app."""
    with Session(engine) as session:
        yield session


def get_current_user(token: str = Header(...),
                     session: Session = Depends(get_session)) -> User:
    """Get the user currently authenticated.

    Parameters
    ----------
    x_token : str
        Authentication token. Get one using the /auth endpoint.

    Returns
    -------
    User
        The user currently authenticated.

    Raises
    ------
    HTTPException
        Raised when the credentials cannot be verified.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token=token,
                             key=AuthSettings().key,
                             algorithms=[AuthSettings().algo])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
        auth_data = TokenData(phone=phone)
    except JWTError as exc:  # TODO : validation error
        raise credentials_exception from exc
    user = UserService(session).read_user_by_phone(auth_data.phone)
    return user
