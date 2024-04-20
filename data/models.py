from pydantic import BaseModel, constr, StringConstraints
from typing_extensions import Annotated

TUsername = Annotated[
    str, StringConstraints(strip_whitespace=True, to_lower=True, pattern='^\w{2,30}$')]  # constr(pattern='^\w{2,30}$')
TPassword = Annotated[
    str, StringConstraints(strip_whitespace=True, pattern='[a-z][A-Z].{6,20}')]  #constr(pattern='[a-z][A-Z].{6,20}')
Temail = Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True,
                                          pattern='^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')]  #constr(pattern='^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')


class User(BaseModel):
    id: int | None = None
    username: TUsername
    password: TPassword | None = None
    role: str = "User"
    firstname: str
    lastname: str
    email: Temail

    # todo is_Admin

    def is_admin(self):
        return self.role == 'Admin'

    @classmethod
    def from_query_result(cls, id, username, password, role, firstname, lastname, email):
        return cls(id=id, username=username, password=password, role=role, firstname=firstname, lastname=lastname,
                   email=email)


class UserView(BaseModel):
    id: int
    username: TUsername
    role: str
    def is_admin(self):
        return self.role == 'Admin'
    @classmethod
    def from_query_result(cls, id, username, role):
        return cls(id=id, username=username, role=role)


class LoginData(BaseModel):
    username: TUsername
    password: TPassword
