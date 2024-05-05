import unittest
from unittest.mock import MagicMock, Mock, patch
from data.models import User, LoginData
from services import user_service as service
from routers import users
from common.responses import BadRequest


def fake_user():
    user = User(id=3, username="test", password="aaaaAA!1234", role="User", firstname="John", lastname="Doe",
         email="test@abv.bg")
    return user

class UserRouter_Should(unittest.TestCase):

    def test_registerEndpointIsSuccessful(self):

        user = fake_user()

        service.check_if_username_exists = MagicMock(return_value=False)
        service.check_if_email_exists = MagicMock(return_value=False)

        service.create = MagicMock(return_value=f"User with id:{user.id} and username:{user.username} was created")

        result = users.register_user(user)

        service.check_if_username_exists.assert_called_once_with(user.username)
        service.check_if_email_exists.assert_called_once_with(user.email)
        service.create.assert_called_once_with(user)
        self.assertEqual("User with id:3 and username:test was created", result)


    @patch("routers.users.user_service.check_if_username_exists")
    @patch("routers.users.user_service.check_if_email_exists")
    def test_registerEndpoint_returnsBadRequestWhenUsernameIsTaken(self, mock_check_if_username_exists, mock_check_if_email_exists):
        user = fake_user()
        mock_check_if_username_exists.return_value = True
        mock_check_if_email_exists.return_value = False
        result = users.register_user(user)

        self.assertIsInstance(result, BadRequest)

    @patch("routers.users.user_service.check_if_username_exists")
    @patch("routers.users.user_service.check_if_email_exists")
    def test_registerEndpoint_returnsBadRequestWhenEmailIsTaken(self, mock_check_if_username_exists, mock_check_if_email_exists):
        user = fake_user()
        mock_check_if_username_exists.return_value = False
        mock_check_if_email_exists.return_value = True
        result = users.register_user(user)

        self.assertIsInstance(result, BadRequest)

    @patch("routers.users.user_service.find_by_username_password")
    @patch("routers.users.auth.create_token")
    def test_loginEndpo_intIsSuccessful(self, mock_create_token, mock_find_by_username_password):
        user = fake_user()
        mock_find_by_username_password.return_value = user
        token = "mock_token"
        mock_create_token.return_value = token

        login_data = LoginData(username=user.username, password=user.password)

        result = users.login(login_data)

        mock_find_by_username_password.assert_called_once_with(user.username, user.password)
        mock_create_token.assert_called_once_with(user)
        self.assertEqual({"token": token}, result)



    @patch("routers.users.user_service.find_by_username_password")
    def test_loginEndpoint_returnsBadRequestWhenUserWitLoginDataNotFound(self, mock_find_by_username_password):
        user = fake_user()
        mock_find_by_username_password.return_value = []

        login_data = LoginData(username=user.username, password=user.password)

        result = users.login(login_data)

        self.assertIsInstance(result, BadRequest)

