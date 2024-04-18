from pydantic import BaseModel, constr


TUsername = constr(pattern='^\w{2,30}$')
TPassword = constr(pattern='[a-z][A-Z].{6,}') # todo check if there is a way to suport this regex:  constr(pattern='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,20}$')
Temail = constr(pattern='^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')
class User(BaseModel):
    id: int | None = None
    username: TUsername
    password: TPassword | None = None
    role: str = "User"
    firstname: str
    lastname: str
    email: Temail

    @classmethod
    def from_query_reslt(cls, id, username, password, role, firstname, lastname, email):
        return cls(id=id, username=username, password=password, role=role, firstname=firstname, lastname=lastname, email=email)


class UserView(BaseModel):
    id: int
    username: TUsername
    role: str

    @classmethod
    def from_query_result(cls,id, username, role):
        return cls(id=id, username=username, role=role)

class LoginData(BaseModel):
    username: TUsername
    password: TPassword