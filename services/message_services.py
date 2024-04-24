from data.models import Message, ViewMessage
from data.database import read_query, insert_query, update_query
from datetime import datetime


def get_all():
    messages = read_query('SELECT id, text, sender_id, date FROM messages')

    return [Message.from_query_result(*row) for row in messages]


def get_by_id(id: int):
    message = read_query(
        'SELECT id, text, sender_id, date FROM messages WHERE sender_id = ?', (id,))
    if not message:
        return None
    
    return [Message.from_query_result(*row) for row in message]


def conversations_by_id(id: int):
    user_message_interactions = read_query('''SELECT mu.receiver_id
                                                FROM messages_users as mu
                                                JOIN messages as m
                                                ON mu.message_id = m.id
                                                WHERE m.sender_id = ?
                                                ORDER BY m.date desc;''', (id,))
    return user_message_interactions

def conversation_between_ids(user_id_1:int, user_id_2:int):
    user_messages: ViewMessage= read_query('''SELECT m.id, m.sender_id, mu.receiver_id, m.text, m.date
                                FROM messages_users mu
                                JOIN messages m
                                ON mu.message_id = m.id
                                WHERE (m.sender_id = ? and mu.receiver_id = ?)
                                OR (m.sender_id = ? and mu.receiver_id = ?)
                                ORDER BY m.date desc;''', (user_id_1, user_id_2, user_id_2, user_id_1))
    return [ViewMessage.from_query_result(*row) for row in user_messages]

def create(message: ViewMessage):
    generated_id = insert_query(
        'INSERT INTO messages(id,text,sender_id,date) VALUES(?,?,?,?)',
        (message.id, message.text,message.sender_id, message.date))

    populate_messages_users = insert_query(
        'INSERT INTO messages_users(message_id,receiver_id) VALUES(?,?)',
        (message.id, message.receiver_id))
    message.id = generated_id
    return message

def exists(id: int):
    return any(
        read_query(
            "SELECT receiver_id FROM messages_users where receiver_id = ?",
            (id,),
        )
    )

