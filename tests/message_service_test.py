import unittest
from unittest.mock import patch
from datetime import datetime
from services import message_services as service
from data.models import ViewMessage, ConversationUserModel


TEST_DATE = datetime(2020, 1, 1, 12, 11, 10)
TEST_CONTENT = "This is a test message."

class ConversationServiceTests(unittest.TestCase):
    
    @patch("services.message_services.read_query")
    def test_conversationsById_returnsAllIDs(self, mock_read_query):
        mock_read_query.return_value = [(1, "user1"), (2, "user2")]
        result = service.conversations_by_id(3)
        expected = ("User 3(you) has conversations with the following users:",
                    [ConversationUserModel(receiver_id=1, username="user1"),
                     ConversationUserModel(receiver_id=2, username="user2")])
        self.assertEqual(expected, result)

    @patch("services.message_services.read_query")
    def test_conversationsById_returnsMessageWhenNoConversations(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.conversations_by_id(3)
        expected = ("There are no current conversations.")
        self.assertEqual(expected, result)


    @patch("services.message_services.read_query")
    def test_conversationBetweenIds_returnsAllMessages(self, mock_read_query):
        mock_read_query.return_value = [(1, 1, TEST_CONTENT, TEST_DATE, 2), (2, 2, "Another text", TEST_DATE, 1)]
        result = service.conversation_between_ids(1, 2)
        expected = [ViewMessage(id=1, sender_id=1, text=TEST_CONTENT, date=TEST_DATE, receiver_id=2,), ViewMessage(id=2, sender_id=2, text="Another text", date=TEST_DATE, receiver_id=1)]
        self.assertEqual(expected, result)

    @patch("services.message_services.read_query")
    def test_conversationBetweenIds_returnsMessageWhenNoMessagesToShow(self, mock_read_query):
        mock_read_query.return_value = []
        result = service.conversation_between_ids(1, 2)
        expected = "There are no messages to show between User 1(you) and User 2"
        self.assertEqual(expected, result)



    @patch("services.message_services.insert_query")
    @patch("services.message_services.datetime")
    def test_create_message(self, mock_datetime, mock_insert_query):
        mock_datetime.now.return_value = TEST_DATE
        mock_insert_query.side_effect = [1, 2]  
        message = ViewMessage(sender_id=1, text=TEST_CONTENT, receiver_id=2)
        result = service.create(message)
        expected = "Message to User 2 successfully sent (ID 1)!"
        self.assertEqual(expected, result)

    @patch("services.message_services.read_query")
    def test_exists_returnsTrueWhenUserExists(self, mock_read_query):
        mock_read_query.return_value = [(1,)]
        result = service.exists(1)
        self.assertTrue(result)

    @patch("services.message_services.read_query")
    def test_exists_returnsFalseWhenUserDoesNotExist(self, mock_read_query):
        mock_read_query.return_value = []
        result = service.exists(1)
        self.assertFalse(result)

