"""This module implements API endpoints handling authentication operations.

Functions
---------
register()
    Register a new user.
get_verify_code()
    Have the server send a verification code.
get_user_token()
    Get an authentication token.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.configs.api_dependencies import get_session
from app.configs.settings import AuthSettings
from app.models.auths import Auth
from app.models.tokens import Token, TokenData
from app.models.users import UserCreate, UserRead
from app.services.auth_services import AuthService
from app.services.user_services import UserService
from app.utils.token_utils import create_access_token
from app.utils.verify_code_utils import create_verify_code, send_verify_code

router = APIRouter()


@router.post(path="/register",
             response_model=UserRead,
             summary="Register a new user.",
             response_description="The created user.")
async def register(*,
                   session: Session = Depends(get_session),
                   user: UserCreate):
    """
    The input user is saved in database, altogether with an Auth object to
    store the phone number for later authentication.

    - **body** : the user to create. Model UserRead.
    """
    return UserService(session).create_user(user)


@router.post(path="/verify_code",
             summary="Send the verification code.",
             response_description="The message when the code is sent.")
async def get_verify_code(*,
                          session: Session = Depends(get_session),
                          data: TokenData):
    """
    Log in the app to have it send the verification token.

    - **body** : the data used to login. Model TokenData.
    """
    phone_number = data.phone
    verify_code = create_verify_code()
    AuthService(session).update_code(phone_number, verify_code)

    sent = send_verify_code()
    if sent is False:
        raise HTTPException(status_code=500,
                            detail="Could not send verify code")

    return {"message", "Verification code sent successfully."}


@router.post(path="/token",
             response_model=Token,
             summary="Get user token.",
             response_description="The authentication token.")
async def get_user_token(*,
                         session: Session = Depends(get_session),
                         auth: Auth):
    """
    Get an authentication token when providing necessary data.

    - **body**: The data to authenticate. Model Auth.
    """
    db_auth = AuthService(session).read_auth_by_phone(auth.phone)
    if db_auth.verify_code != auth.verify_code:
        raise HTTPException(status_code=400,
                            detail="Invalid verification code.")

    access_token_expires = timedelta(minutes=AuthSettings().token_exp)
    access_token = create_access_token(
        data={"sub": db_auth.phone},
        expires_delta=access_token_expires
    )
    resp_token = Token(access_token=access_token, token_type="bearer")
    return resp_token


# @router.get("/users", response_model=List[UserRead])
# def read_users(*,
#                session: Session = Depends(get_session),
#                offset: int = 0,
#                limit: int = Query(default=100, lte=100)):
#     return UserService(session).read_users(offset, limit)
