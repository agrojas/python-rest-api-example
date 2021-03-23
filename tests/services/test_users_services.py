from app.services.users_service import UsersService


def test_get_users_is_not_empty():
    us = UsersService()
    assert us.get_users()
