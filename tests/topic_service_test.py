import unittest
from unittest.mock import Mock, patch
from data.models import Topic
from services import topic_service


# Constants for testing
TEST_TITLE = "Test Topic"
TEST_CATEGORY = 1
TEST_USER_ID = 1
TEST_DATE = '2024-05-03'
TEST_DESCRIPTION = "test description"
TEST_STATUS = "unlocked"
TEST_BEST_REPLY = "This is the best reply!"


def create_topic(topic_id):
    return Topic(
        id=topic_id,
        title=TEST_TITLE,
        category_id=TEST_CATEGORY,
        description=TEST_DESCRIPTION
    )


def create_topic_view(topic_id):
    return Topic.from_query_result(
        id=topic_id,
        title=TEST_TITLE,
        category_id=TEST_CATEGORY,
        user_id=TEST_USER_ID,
        date=TEST_DATE,
        description=TEST_DESCRIPTION,
        is_locked=TEST_STATUS,
        best_reply=TEST_BEST_REPLY
    )


class TopicServices_Should(unittest.TestCase):
    def test_getById_returnsCorrectTopic(self):
        with patch("services.topic_service.read_query") as get_topic_func:
            test_id = 2
            get_topic_func.return_value = [
                (
                    test_id,
                    TEST_TITLE,
                    TEST_CATEGORY,
                    TEST_USER_ID,
                    TEST_DATE,
                    TEST_DESCRIPTION,
                    TEST_STATUS,
                    TEST_BEST_REPLY
                )
            ]

            expected = create_topic_view(test_id)
            result = topic_service.get_by_id(test_id)
            self.assertEqual(expected, result)

    def test_getById_returnsNone(self):
        with patch("services.topic_service.read_query") as get_topic_func:
            test_id = 2
            get_topic_func.return_value = []

            result = topic_service.get_by_id(test_id)
            self.assertIsNone(result)



    def test_exists_returnsTrue(self):
        with patch("services.topic_service.read_query") as get_topic_func:
            test_id = 2
            get_topic_func.return_value = [
                (
                    test_id,
                    TEST_TITLE,
                    TEST_CATEGORY,
                    TEST_USER_ID,
                    TEST_DATE,
                    TEST_DESCRIPTION,
                    TEST_STATUS,
                    TEST_BEST_REPLY
                )
            ]

            result = topic_service.exists(test_id)
            self.assertTrue(result)

    def test_exists_returnsFalse(self):
        with patch("services.topic_service.read_query") as get_topic_func:
            test_id = 2
            get_topic_func.return_value = []

            result = topic_service.exists(test_id)
            self.assertFalse(result)

    def test_create_returnsCorrectTopic(self):
        with patch("services.topic_service.insert_query") as create_topic_func:
            create_topic_func.return_value = 2
            test_topic = create_topic(2)
            expected = Topic(
                id=test_topic.id,
                title=TEST_TITLE,
                category_id=TEST_CATEGORY,
                description=TEST_DESCRIPTION
            )
            result = topic_service.create(test_topic)
            self.assertEqual(expected, result)



