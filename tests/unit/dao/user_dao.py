
from datetime import date as dt
from sqlmodel import Session

from app.dao.user_dao import UserDao
from app.models.users import User


class TestUserCreate:
    """Contains tests related to user creation"""

    def test_create_user_full(session: Session):
        """Test creating a User with full body input."""
        user = User(
            phone="+33604202269",
            first_name="Jane",
            last_name="Doe",
            bio="Mysterious woman.",
            city="NYC"
        )

        db_user = UserDao(session).create_user(user)

        assert db_user.phone == user.phone
        assert db_user.first_name == user.first_name
        assert db_user.last_name == user.last_name
        assert db_user.bio == user.bio
        assert db_user.city == user.city
        assert db_user.register_date == dt.today()
        assert isinstance(db_user.id, int)
    
    def test_create_user_partial_valid(session: Session):
        """Test that creating a user with partial info works if only optional
        attributes are not set."""
    
    def test_create_user_partial_invalid(session: Session):
        """Test that creating a user with missing info raises
        the right Exception."""
    
    def test_create_user_invalid_phone(session: Session):
        """Test that creating with a wrong phone number fails."""
    
    def test_create_user_same_phone(session: Session):
        """Same but with a phone that exists from another account."""