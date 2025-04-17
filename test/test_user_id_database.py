import pytest
from datetime import datetime, timedelta
from grokautogen.invest.user_id_database import User, Cookie, UserDB
from passlib.hash import bcrypt


def test_user_creation_with_password() -> None:
    user = User(user_id="test_user", password="test_password")
    assert user.user_id == "test_user"
    assert bcrypt.verify("test_password", user.password_hash)
    assert user.active is True
    assert isinstance(user.since, datetime)


def test_user_creation_with_password_hash() -> None:
    password_hash = bcrypt.hash("test_password")
    user = User(user_id="test_user", password_hash=password_hash)
    assert user.user_id == "test_user"
    assert user.password_hash == password_hash
    assert user.active is True


def test_user_password_verification() -> None:
    user = User(user_id="test_user", password="test_password")
    assert user.verify_password("test_password") is True
    assert user.verify_password("wrong_password") is False


def test_cookie_save_and_load() -> None:
    user = User(user_id="test_user", password="test_password")
    cookie = Cookie()
    cookie.save(user)
    loaded_cookie: Cookie = Cookie.load(user)
    assert abs(loaded_cookie.last_login - cookie.last_login) < timedelta(seconds=1)


def test_cookie_expired() -> None:
    cookie = Cookie(last_login=datetime.now() - timedelta(hours=2))
    assert cookie.expired() is True
    cookie = Cookie(last_login=datetime.now())
    assert cookie.expired() is False


def test_userdb_add_user() -> None:
    db = UserDB()
    user = User(user_id="test_user", password="test_password")
    db.add_user(user)
    assert len(db.users) == 1
    assert db.users[0].user_id == "test_user"
    assert db.users[0].verify_password("test_password")


def test_userdb_add_duplicate_user() -> None:
    db = UserDB()
    user = User(user_id="test_user", password="test_password")
    db.add_user(user)
    with pytest.raises(ValueError, match="User ID 'test_user' already exists"):
        db.add_user(user)


def test_userdb_authenticate() -> None:
    db = UserDB()
    user = User(user_id="test_user", password="test_password")
    db.add_user(user)
    assert db.authenticate("test_user", "test_password") is True
    assert db.authenticate("test_user", "wrong_password") is False
    assert db.authenticate("nonexistent_user", "test_password") is False


def test_userdb_save_and_load(tmp_path) -> None:
    db = UserDB()
    user = User(user_id="test_user", password="test_password")
    db.add_user(user)
    filepath = tmp_path / "user.json"
    db.save(filepath)
    loaded_db: UserDB = UserDB.load(filepath)
    assert len(loaded_db.users) == 1
    assert loaded_db.users[0].user_id == "test_user"
    assert loaded_db.users[0].verify_password("test_password")
