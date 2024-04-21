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

#class ConvoResponse with list of msgs
def conversation(id: int):
    user = get_by_id(id)
    user_messages = read_query('''SELECT m.id, m.sender_id, mu.receiver_id, m.text, m.date
                                FROM forum_app.messages_users mu
                                JOIN forum_app.messages m
                                ON mu.message_id = m.id
                                WHERE m.sender_id = ?
                                OR mu.receiver_id = ?
                               ''', (id, id))

    conversations = [ViewMessage.from_query_result(*row) for row in user_messages]

    # user_sent_to = read_query('''SELECT mu.receiver_id
    #                             FROM forum_app.messages_users mu
    #                             join
    #                             forum_app.messages m
    #                             on 
    #                             mu.message_id = m.id
    #                             where m.sender_id = ?''', (id)) # 3
    
    # user_received_by = read_query('''SELECT m.sender_id
    #                             FROM forum_app.messages_users mu
    #                             join
    #                             forum_app.messages m
    #                             on 
    #                             mu.message_id = m.id
    #                             where mu.receiver_id = ?''', [row for row in user_sent_to]) #
    
    # if not conversation:
    #     return None

    # return [Message.from_query_result(*row) for row in message]

