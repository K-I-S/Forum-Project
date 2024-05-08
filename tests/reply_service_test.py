import unittest
from unittest.mock import patch
from datetime import date, datetime
from data.models import Reply, ReplyView, UserVote
from services import reply_service as service

TEST_DATE = datetime(2020, 1, 1, 12, 11, 10)
TEST_CONTENT = "Test reply for topic"

def fake_reply_view():
    return ReplyView.from_query_result(
        id=1,
    user_id=2,
    date=TEST_DATE,
    topic_id=3,
    content=TEST_CONTENT,
    upvotes=2,
    downvotes=1,)

def fake_reply():
    return Reply(id=1, user_id=2, date=TEST_DATE, topic_id=3, content=TEST_CONTENT)

def fake_user_vote():
    return UserVote.from_query_result(id=1, user_id=2, vote_type="up", replies_id=2)

class ReplyService_Should(unittest.TestCase):

    @patch("services.reply_service.read_query")
    def test_getByTopic_returnsAllRepliesForTopic(self, mock_read_query):
        mock_read_query.return_value = [(1, 2, TEST_DATE, 3, TEST_CONTENT, 2, 1), (2, 3, TEST_DATE, 3, TEST_CONTENT, 3, 4)]

        result = service.get_by_topic(3)
        result = list(result)
        fake_rep2 = fake_reply_view()
        fake_rep2.id = 2
        fake_rep2.user_id = 3
        fake_rep2.upvotes = 3
        fake_rep2.downvotes = 4

        expected = [fake_reply_view(), fake_rep2]
        mock_read_query.assert_called_once_with(
        """
    SELECT 
        r.id, r.user_id, r.date, r.topic_id, r.content,
        COUNT(CASE WHEN uv.vote_type = 1 THEN 1 END) AS upvotes,
        COUNT(CASE WHEN uv.vote_type = 0 THEN 1 END) AS downvotes
    FROM 
        replies r
    LEFT JOIN 
        user_votes uv ON r.id = uv.replies_id
    WHERE 
        r.topic_id = ?
    GROUP BY 
        r.id
    """,
        (3,),
    )
        self.assertEqual(expected, result)

    @patch("services.reply_service.read_query")
    def test_getByTopic_returnsEmptyListWhenNoRepliesFound(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.get_by_topic(3)
        result = list(result)

        expected = []
        mock_read_query.assert_called_once_with(
        """
    SELECT 
        r.id, r.user_id, r.date, r.topic_id, r.content,
        COUNT(CASE WHEN uv.vote_type = 1 THEN 1 END) AS upvotes,
        COUNT(CASE WHEN uv.vote_type = 0 THEN 1 END) AS downvotes
    FROM 
        replies r
    LEFT JOIN 
        user_votes uv ON r.id = uv.replies_id
    WHERE 
        r.topic_id = ?
    GROUP BY 
        r.id
    """,
        (3,),
    )
        self.assertEqual(expected, result)


    @patch("services.reply_service.read_query")
    def test_getById_returnsCorrectReply(self, mock_read_query):
        mock_read_query.return_value = [(1, 2, TEST_DATE, 3, TEST_CONTENT)]

        result = service.get_by_id(3)

        mock_read_query.assert_called_once_with("select id, user_id, date, topic_id, content from replies where id = ?", (3,))
        self.assertEqual(fake_reply(), result)

    @patch("services.reply_service.read_query")
    def test_getById_returnsNoneWhenNoReplyFound(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.get_by_id(3)

        mock_read_query.assert_called_once_with("select id, user_id, date, topic_id, content from replies where id = ?", (3,))
        self.assertIsNone(result)

    @patch("services.reply_service.read_query")
    def test_exists_returnsTrueWhenRepyIsFound(self, mock_read_query):
        mock_read_query.return_value = [(1, 2, TEST_DATE, 3, TEST_CONTENT)]
        result = service.get_by_id(3)
        self.assertTrue(result)

    @patch("services.reply_service.read_query")
    def test_exists_returnsFalseWhenRepyIsNotFound(self, mock_read_query):
        mock_read_query.return_value = []
        result = service.get_by_id(3)
        self.assertFalse(result)

    @patch("services.reply_service.insert_query")
    @patch("services.reply_service.datetime")
    def test_create_reply(self, mock_datetime, mock_insert_query):
        mock_datetime.now.return_value = TEST_DATE
        mock_insert_query.return_value = 1

        result = service.create(3, 1, TEST_CONTENT)

        mock_insert_query.assert_called_once_with(
        "insert into replies (user_id, date, topic_id, content) values(?,?,?,?)",
        (1, '2020-01-01 12:11:10', 3, TEST_CONTENT),
    )
        self.assertEqual(1, result)

    @patch("services.reply_service.insert_query")
    def test_createUserVote_returnsCallsCorrectQueryWhenVoteISUP(self, mock_insert_query):

        result = service.create_user_vote(3, "up", 1)
        mock_insert_query.assert_called_once_with(
        "insert into user_votes (user_id, vote_type, replies_id) values (?,?,?)",
        (3, 1, 1),
    )

    @patch("services.reply_service.insert_query")
    def test_createUserVote_returnsCallsCorrectQueryWhenVoteISDOWN(self, mock_insert_query):

        result = service.create_user_vote(3, "down", 1)
        mock_insert_query.assert_called_once_with(
        "insert into user_votes (user_id, vote_type, replies_id) values (?,?,?)",
        (3, 0, 1),
    )

    @patch("services.reply_service.read_query")
    def test_getUserVote_returnsUserVoteWhenFound(self, mock_read_query):
        mock_read_query.return_value = [(1, 2, "up", 2)]
        result = service.get_user_vote(2, 2)
        mock_read_query.assert_called_once_with(
        "select id, user_id, vote_type, replies_id from user_votes where user_id = ? and replies_id = ?",
        (2, 2),
    )

        self.assertEqual(fake_user_vote(), result)

    @patch("services.reply_service.read_query")
    def test_getUserVote_returnsNoneWhenNotFound(self, mock_read_query):
        mock_read_query.return_value = []
        result = service.get_user_vote(2, 2)
        mock_read_query.assert_called_once_with(
        "select id, user_id, vote_type, replies_id from user_votes where user_id = ? and replies_id = ?",
        (2, 2),
    )

        self.assertIsNone(result)

    @patch("services.reply_service.update_query")
    def test_updateVote_CallsCorrectQueryWhenVoteIsUP(self, mock_update_query):
        service.update_vote(1, "up")
        mock_update_query.assert_called_once_with(
        "update user_votes set vote_type = ? where id = ?",
        (1, 1),)

    @patch("services.reply_service.update_query")
    def test_updateVote_CallsCorrectQueryWhenVoteIsDown(self, mock_update_query):
        service.update_vote(1, "down")
        mock_update_query.assert_called_once_with(
        "update user_votes set vote_type = ? where id = ?",
        (0, 1),)