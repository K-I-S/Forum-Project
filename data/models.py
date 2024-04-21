from pydantic import BaseModel, constr, Field, StringConstraints
from typing import Annotated
from datetime import datetime


class Message(BaseModel):
    id: int
    text: str
    sender_id: int
    date: datetime

    @classmethod
    def from_query_result(cls, id, text,sender_id,date):
        return cls(
            id=id,
            text=text,
            sender_id=sender_id,
            date=date)
    

class ViewMessage(BaseModel):
    id: int
    sender_id: int
    receiver_id: int 
    text: str
    date: datetime

    @classmethod
    def from_query_result(cls, id, sender_id,receiver_id,text,date):
        return cls(
            id=id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            text=text,
            date=date)




