from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime

TUsername = Annotated[
    str, StringConstraints(strip_whitespace=True, to_lower=True, pattern=r"^\w{2,30}$")
]
TPassword = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, pattern=r"[a-zA-Z0-9._%-].{6,20}"
    ),  # Todo make better regex
    str,
    StringConstraints(
        strip_whitespace=True, pattern=r"[a-zA-Z0-9._%-].{6,20}"
    ),  # Todo make better regex
]
Temail = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        pattern=r"^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$",
    ),
]


class User(BaseModel):
    id: int | None = None
    username: TUsername
    password: TPassword
    role: str = "User"
    firstname: str
    lastname: str
    email: Temail

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
    
class PrivilegedUserView(BaseModel):
    id: int
    access_type: Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, to_lower=True, pattern=r"^(read|write)$"
            ),
        ]
    
    @classmethod
    def from_query_result(cls, id, access_type):
        return cls(id=id, access_type="write" if access_type else "read")
    


class LoginData(BaseModel):
    username: TUsername
    password: TPassword

class UserAccess(BaseModel):
    categories_id: int
    users_id: int
    access_type: (
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, to_lower=True, pattern=r"^(read|write)$"
            ),
        ]
        | None
    ) = None

    def has_read_access(self):
        return self.access_type == "read"
    
    def has_write_access(self):
        return self.access_type == "write"
    
    @classmethod
    def from_query_result(cls, categories_id, users_id, access_type):
        return cls(
            categories_id=categories_id,
            users_id=users_id,
            access_type="write" if access_type else "read"
        )


class Category(BaseModel):
    id: int | None = None
    name: Annotated[str, StringConstraints(min_length=2)]
    description: str | None = None
    status: (
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, to_lower=True, pattern=r"^(unlocked|locked)$"
            ),
        ]
        | None
    ) = None
    privacy: (
        Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, to_lower=True, pattern=r"^(public|private)$"
            ),
        ]
        | None
    ) = None

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
    user_id: int | None = None
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
    user_id: int | None = None
    date: datetime | None = None
    topic_id: int
    content: str

    @classmethod
    def from_query_result(
        cls,
        id,
        user_id,
        date,
        topic_id,
        content,
    ):
        return cls(
            id=id,
            user_id=user_id,
            date=date,
            topic_id=topic_id,
            content=content,
        )


class ReplyView(BaseModel):
    id: int | None = None
    user_id: int | None = None
    date: datetime | None = None
    topic_id: int
    content: str
    upvotes: int | None = None
    downvotes: int | None = None

    @classmethod
    def from_query_result(
        cls, id, user_id, date, topic_id, content, upvotes, downvotes
    ):
        return cls(
            id=id,
            user_id=user_id,
            date=date,
            topic_id=topic_id,
            content=content,
            upvotes=upvotes,
            downvotes=downvotes,
        )


class UserVote(BaseModel):
    id: int | None = None
    user_id: int
    vote_type: Annotated[
        str,
        StringConstraints(strip_whitespace=True, to_lower=True, pattern=r"^(up|down)$"),
    ]
    replies_id: int

    @classmethod
    def from_query_result(cls, id, user_id, vote_type, replies_id):
        return cls(
            id=id,
            user_id=user_id,
            vote_type="up" if vote_type else "down",
            replies_id=replies_id,
        )


class CategoryResponseModel(BaseModel):
    category: Category
    topics: list[Topic]


class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[ReplyView]

class CategoryPrivilegedUsers(BaseModel):
    category: Category
    users: list[PrivilegedUserView]



class ViewMessage(BaseModel):
    id: int | None = None
    sender_id: int | None = None
    text: str
    date: datetime | None = None
    receiver_id: int

    @classmethod
    def from_query_result(cls, id, sender_id, text, date, receiver_id):
        return cls(
            id=id, sender_id=sender_id, receiver_id=receiver_id, text=text, date=date
        )

class ConversationUserModel(BaseModel):
    receiver_id: int
    username: str