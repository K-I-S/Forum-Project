from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime

TUsername = Annotated[
    str, StringConstraints(strip_whitespace=True, to_lower=True, pattern="^\w{2,30}$")
]
TPassword = Annotated[
    str, StringConstraints(strip_whitespace=True, pattern="[a-z][A-Z].{6,20}")
]
Temail = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        pattern="^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$",
    ),
]


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
        return self.role == "Admin"

    @classmethod
    def from_query_result(
        cls, id, username, password, role, firstname, lastname, email
    ):
        return cls(
            id=id,
            username=username,
            password=password,
            role=role,
            firstname=firstname,
            lastname=lastname,
            email=email,
        )


class UserView(BaseModel):
    id: int
    username: TUsername
    role: str

    def is_admin(self):
        return self.role == "Admin"

    @classmethod
    def from_query_result(cls, id, username, role):
        return cls(id=id, username=username, role=role)


class LoginData(BaseModel):
    username: TUsername
    password: TPassword


class Category(BaseModel):
    id: int | None = None
    name: Annotated[str, StringConstraints(min_length=2)]
    description: str
    status: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, to_lower=True, pattern=r"^(unlocked|locked)$"
        ),
    ]
    privacy: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, to_lower=True, pattern=r"^(public|private)$"
        ),
    ]

    def is_locked(self):
        return self.status == "locked"

    def is_private(self):
        return self.privacy == "private"

    @classmethod
    def from_query_result(cls, id, name, description, is_locked, is_private):
        return cls(
            id=id,
            name=name,
            description=description,
            status="locked" if is_locked else "unlocked",
            privacy="private" if is_private else "public",
        )


class Topic(BaseModel):
    id: int | None = None
    title: Annotated[str, StringConstraints(min_length=2)]
    category_id: int
    user_id: int
    date: datetime | None = None
    description: str
    status: (
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, to_lower=True, pattern=r"^(unlocked|locked)$"
            ),
        ]
        | None
    ) = None
    best_reply: int | str | None = None

    def is_locked(self):
        return self.status == "locked"

    @classmethod
    def from_query_result(
        cls,
        id,
        title,
        category_id,
        user_id,
        date,
        description,
        is_locked,
        best_reply,
    ):
        return cls(
            id=id,
            title=title,
            category_id=category_id,
            user_id=user_id,
            date=date,
            description=description,
            status="locked" if is_locked else "unlocked",
            best_reply=best_reply if best_reply else "no best reply yet",
        )


class Reply(BaseModel):
    id: int | None = None
    user_id: int
    date: datetime | None = None
    topic_id: int
    content: str

    @classmethod
    def from_query_result(cls, id, user_id, date, topic_id, content):
        return cls(
            id=id, user_id=user_id, date=date, topic_id=topic_id, content=content
        )


class CategoryResponseModel(BaseModel):
    category: Category
    topics: list[Topic]


class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]
