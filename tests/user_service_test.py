import unittest
from unittest.mock import patch
from data.models import User, UserView
from services import user_service as service

TEST_EMAIL = "test_mail@test.com"
TEST_USERNAME = "Test_Username"
TEST_PASSWORD = "<PASSWORD>"

def fake_user():
    return User( id= 1,
    username = TEST_USERNAME,
    password = TEST_PASSWORD,
    role = "User",
    firstname = "Test_Firstname",
    lastname = "Test_Lastname",
    email = TEST_EMAIL)

def fake_user_view():
    return UserView.from_query_result(id=1, username=TEST_USERNAME, role="User")

class UserService_Should(unittest.TestCase):

    @patch('services.user_service.read_query')
    def test_checkIfUsernameExists_returnsUserViewWhenUserIsFound(self, mock_read_query):
        mock_read_query.return_value = [(1, "Test_Username", "User")]

        result = service.check_if_username_exists(TEST_USERNAME)

        mock_read_query.assert_called_once_with("select id, username, role from users where username = ?", (TEST_USERNAME,))

        self.assertEqual(fake_user_view(), result)

    @patch('services.user_service.read_query')
    def test_checkIfUsernameExists_returnsNoneWhenUserIsNotFound(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.check_if_username_exists(TEST_USERNAME)

        mock_read_query.assert_called_once_with("select id, username, role from users where username = ?", (TEST_USERNAME,))

        self.assertIsNone(result)

    @patch('services.user_service.read_query')
    def test_checkIfEmailExists_returnsUserViewWhenUserIsFound(self, mock_read_query):
        mock_read_query.return_value = [(1, "Test_Username", "User")]

        result = service.check_if_email_exists(TEST_EMAIL)

        mock_read_query.assert_called_once_with("select id, username, role from users where email = ?", (TEST_EMAIL,))

        self.assertEqual(fake_user_view(), result)

    @patch('services.user_service.read_query')
    def test_checkIfEmailExists_returnsNoneWhenUserIsNotFound(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.check_if_email_exists(TEST_EMAIL)

        mock_read_query.assert_called_once_with("select id, username, role from users where email = ?", (TEST_EMAIL,))

        self.assertIsNone(result)

    @patch('services.user_service.hash_pass')
    @patch('services.user_service.insert_query')
    def test_create_returnsMessageWhenUserIsCreated(self, mock_insert_query, mock_hash_pass):
        mock_hash_pass.return_value = "Hashed_password"
        mock_insert_query.return_value = 1
        user = fake_user()
        result = service.create(user)

        mock_hash_pass.assert_called_once_with(TEST_PASSWORD)
        mock_insert_query.assert_called_once_with("INSERT INTO users(username, password, firstname, lastname, email) VALUES(?,?,?,?,?)",
                                (user.username, "Hashed_password", user.firstname, user.lastname, user.email))

        expected = f"User with id:1 and username:test_username was created"
        self.assertEqual(expected, result)


    @patch('services.user_service.hash_pass')
    @patch('services.user_service.read_query')
    def test_findByUsernamePassword_returnsUserViewWhenUserIsFound(self, mock_read_query, mock_hash_pass):
        mock_hash_pass.return_value = "Hashed_password"
        mock_read_query.return_value = [(1, "Test_Username", "User")]

        result = service.find_by_username_password(TEST_USERNAME, TEST_PASSWORD)

        mock_hash_pass.assert_called_once_with(TEST_PASSWORD)
        mock_read_query.assert_called_once_with("select id, username, role from users where username = ? and password = ?",
                           (TEST_USERNAME, "Hashed_password"))
        self.assertEqual(fake_user_view(), result)


    @patch('services.user_service.hash_pass')
    @patch('services.user_service.read_query')
    def test_findByUsernamePassword_returnsNoneWhenUserIsNotFound(self, mock_read_query, mock_hash_pass):
        mock_hash_pass.return_value = "Hashed_password"
        mock_read_query.return_value = []

        result = service.find_by_username_password(TEST_USERNAME, TEST_PASSWORD)

        mock_hash_pass.assert_called_once_with(TEST_PASSWORD)
        mock_read_query.assert_called_once_with("select id, username, role from users where username = ? and password = ?",
                           (TEST_USERNAME, "Hashed_password"))
        self.assertIsNone(result)
