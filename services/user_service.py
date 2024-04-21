from data.models import User, UserView, LoginData
from data.database import read_query, insert_query, update_query
from hashlib import sha256
import jwt

_SECRET = "kisKIS123"
def hash_pass(password):
    hashed_password = sha256(password.encode("utf-8")).hexdigest()
    return hashed_password
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

def create_token(user: User) -> str:
    payload = {user.id: user.id, user.username: user.username} #todo Double check if its made correctly

    encoded = jwt.encode(payload, _SECRET, algorithm="HS256")
    return encoded

def is_authenticated(token: str) -> bool:
    user_id, username = jwt.decode(token, _SECRET, algorithms="HS256")

    user_data = read_query("select id, username, role from users where id = ? and username = ?",
                           (user_id, username))

    if next((UserView.from_query_result(*row) for row in user_data), None):
        return True
    return False

def from_token(token: str) -> User | None:
    user_id, username = jwt.decode(token, _SECRET, algorithms="HS256")
    user = check_if_username_exists(username)

    return user