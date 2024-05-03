from data.models import User, UserView
from data.database import read_query, insert_query
from common.auth import hash_pass


def check_if_username_exists(username: str):
    user_exists = read_query("select id, username, role from users where username = ?", (username,))
    return next((UserView.from_query_result(*row) for row in user_exists), None)


def check_if_email_exists(email: str):
    user_exists = read_query("select id, username, role from users where email = ?", (email,))
    return next((UserView.from_query_result(*row) for row in user_exists), None)


def create(user: User):
    user_pass = hash_pass(user.password)
    generated_id = insert_query("INSERT INTO users(username, password, firstname, lastname, email) VALUES(?,?,?,?,?)",
                                (user.username, user_pass, user.firstname, user.lastname, user.email))
    return f"User with id:{generated_id} and username:{user.username} was created"


def find_by_username_password(username: str, password: str) -> User | None:
    new_pass = hash_pass(password)
    user_data = read_query("select id, username, role from users where username = ? and password = ?",
                           (username, new_pass))
    return next((UserView.from_query_result(*row) for row in user_data), None)
