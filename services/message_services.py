from data.models import ViewMessage, ConversationUserModel
from data.database import read_query, insert_query
from datetime import datetime



def conversations_by_id(id: int):
    user_message_interactions = read_query('''SELECT DISTINCT mu.receiver_id, u.username
                                                FROM messages_users as mu
                                                JOIN messages as m
                                                ON mu.message_id = m.id
                                                JOIN users as u
                                                ON u.id = mu.receiver_id
                                                WHERE m.sender_id = ?;''', (id,))

    conversation_list = [
        ConversationUserModel(receiver_id=receiver_id, username=username) for receiver_id, username in user_message_interactions
    ]
    if conversation_list == []:
        return f"There are no current conversations."
    else: 
        return f"User {id}(you) has conversations with the following users:", conversation_list


def conversation_between_ids(user_id_1:int, user_id_2:int):
    user_messages: list[ViewMessage] = read_query('''SELECT m.id, m.sender_id, m.text, m.date,mu.receiver_id
                                FROM messages_users mu
                                JOIN messages m
                                ON mu.message_id = m.id
                                WHERE (m.sender_id = ? and mu.receiver_id = ?)
                                OR (m.sender_id = ? and mu.receiver_id = ?)
                                ORDER BY m.date desc;''', (user_id_1, user_id_2, user_id_2, user_id_1))
    
    if user_messages == []:
        return f"There are no messages to show between User {user_id_1}(you) and User {user_id_2}"
    else: 
        return [ViewMessage.from_query_result(*row) for row in user_messages]


def create(message: ViewMessage):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    generated_id = insert_query(
        'INSERT INTO messages(text,sender_id,date) VALUES(?,?,?)',
        (message.text, message.sender_id, current_time))
    message.id = generated_id
    insert_query(
        'INSERT INTO messages_users(message_id,receiver_id) VALUES(?,?)',
        (message.id, message.receiver_id))

    return f'Message to User {message.receiver_id} successfully sent!'


def exists(id: int):
    return any(
        read_query(
            "SELECT id FROM users where id = ?",
            (id,),
        )
    )