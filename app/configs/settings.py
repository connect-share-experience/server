"""This module implements classes to access all settings needed in app.

These settings can either be created here, or fetched from the dotenv file
at predefined path. Usually, security or architechture dependant settings will
be fetched from environment, while code and external module settings will be
defined inside the classes.

Classes
-------
DBSettings
    Contains all necessary settings relative to the database.
"""

from pathlib import Path

from pydantic import BaseSettings, Field

PATH_TO_DOTENV = "app/.env"


class _BaseAppSettings(BaseSettings):
    """Main parent Settings class.

    This class shall not be instanciated, it exists to ensure that all Settings
    classes share the same Config.
    """
    class Config:
        """Configuration for the settings.

        Attributes
        ----------
        env_file: str
            Sets the path to the dotenv file to load variables from.
        """
        env_file = PATH_TO_DOTENV


class DBSettings(_BaseAppSettings):
    """Contains settings for the database.

    Attributes
    ----------
    path: Path
        The path to the database, i.e the .db file. From env.
    saves_dir: Path
        The path to the directory in which to store database saves. From env.
    echo: bool
        True if the SQL operations should print in terminal. False otherwise.
    thread: bool
        True if we allow multiple requests to use the same session.
        False otherwise.
    """
    path: Path = Field(..., env="PATH_TO_DATABASE")
    saves_dir: Path = Field(..., env="PATH_TO_SAVES_DIR")

    echo: bool = True
    thread: bool = False

    @property
    def url(self) -> str:
        """Get the URL to the database.

        Depending on what kind of database you are using, you might want to
        change the prefix of that URL.
        In this instance, we use sqlite, so we use the "sqlite:///" prefix.

        Returns
        -------
        str
            The database url
        """
        return f"sqlite:///{str(self.path)}"


class APISettings(_BaseAppSettings):
    """Contains settings for the API.

    Attributes
    ----------
    api_host: str
        Host to use for the API.
    api_port: int
        Port to use for the API
    """
    api_host: str = Field(..., env="API_HOST")
    api_port: int = Field(..., env="API_PORT")

    api_reload: bool = True


class AuthSettings(_BaseAppSettings):
    """Contains settings used for authentication.

    Attributes
    ----------
    key: str
        Secret key used for tokens.
    algo: str
        Algorithm used for tokens.
    token_exp: int
        Number of minutes before the token expires.
    """
    key: str = Field(..., env="SECRET_KEY")
    algo: str = Field(..., env="ALGORITHM")
    token_exp: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")


class ExtResourcesSettings(_BaseAppSettings):
    """Contains settings related to external resources, API keys and such.

    Attributes
    ----------
    gmaps_key: str
        Secret key for Google Maps API.
    """
    gmaps_key: str = Field(..., env="GOOGLE_MAPS_KEY")


class StaticSettings(_BaseAppSettings):
    """Contains settings related to handling static files.

    Attributes
    ----------
    user_page_pic_dir: str
        Path to directory containing user profile pictures.
    event_page_pic_dir: str
        Path to directory containing event page pictures.
    """
    user_page_pic_dir: str = "static/images/user_page"
    event_page_pic_dir: str = "static/images/event_page"
