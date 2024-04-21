from data.models import Message, ViewMessage
from data.database import read_query, insert_query, update_query
from datetime import datetime


def get_all():
    messages = read_query('SELECT id, text, sender_id, date FROM messages')

    return [Message.from_query_result(*row) for row in messages]


def get_by_id(id: int):
    message = read_query(
        'SELECT id, text, sender_id, date FROM messages WHERE id = ?', (id,))
    if not message:
        return None
    
    return [Message.from_query_result(*row) for row in message]


def conversations_by_id(id: int):
    user_message_interactions = read_query('''SELECT m.sender_id
                                FROM messages m
                                where m.sender_id = ?''', (id))
    #Ccheck whether to create a list with more comprehensive details of the users with which the authenticated user has had conversations
    return user_message_interactions

def conversation_between_ids(user_id_1:int, user_id_2:int):
    user_messages= read_query('''SELECT m.id, m.sender_id, mu.receiver_id, m.text, m.date
                                FROM forum_app.messages_users mu
                                JOIN forum_app.messages m
                                ON mu.message_id = m.id
                                WHERE (m.sender_id = ? and mu.receiver_id = ?)
                                OR ( m.sender_id = ? and mu.receiver_id = ?)
                                ORDER BY date desc;''', (user_id_1, user_id_2, user_id_2, user_id_1))
    return user_messages

def create(message: Message):
    # !NB - how do I add the receiver_ids to the database/where do I provide them as params
    generated_id = insert_query(
        'INSERT INTO messages(id,text,sender_id,date) VALUES(?,?,?,?)',
        (message.id, message.text,message.sender_id, message.date))
    message.id = generated_id

    return message

