import unittest
from unittest.mock import Mock, patch
from data.models import Category
from services import category_service as service

TEST_NAME = "Test Category"
TEST_STATUS = "unlocked"
TEST_PRIVACY = "public"
TEST_DESCRIPTION = "test description"

def create_category(category_id):
    return Category(
        id=category_id,
        name=TEST_NAME,
        status=TEST_STATUS,
        privacy=TEST_PRIVACY

    )
def create_category_view(category_id):
    return Category.from_query_result(
        id=category_id,
        name=TEST_NAME,
        description=TEST_DESCRIPTION,
        is_locked=TEST_STATUS,
        is_private=TEST_PRIVACY

    )

class CategoryServices_Should(unittest.TestCase):

    def test_getById_returnsCorrectCategory(self):
        with patch("services.category_service.read_query") as get_category_func:
            test_id = 2
            get_category_func.return_value = [(test_id, TEST_NAME, TEST_DESCRIPTION, TEST_STATUS, TEST_PRIVACY)]

            expected = create_category_view(test_id)

            result = service.get_by_id(test_id)

            self.assertEqual(expected, result)

    def test_getById_returnsNone(self):
        with patch("services.category_service.read_query") as get_category_func:
            test_id = 2

            get_category_func.return_value = []

            result = service.get_by_id(test_id)

            self.assertIsNone(result)

    def test_exists_returnsTrue(self):
        with patch("services.category_service.read_query") as get_category_func:
            test_id = 2
            get_category_func.return_value = [(test_id, TEST_NAME, TEST_DESCRIPTION, TEST_STATUS, TEST_PRIVACY)]

            result = service.exists(test_id)

            self.assertTrue(result)

    def test_exists_returnsFalse(self):
        with patch("services.category_service.read_query") as get_category_func:
            test_id = 2
            get_category_func.return_value = []

            result = service.exists(test_id)

            self.assertFalse(result)

    def test_create_returnsCorrectCategory(self):
        with patch("services.category_service.insert_query") as create_category_func:

            create_category_func.return_value = 2

            test_category = create_category(2)

            expected = Category(id=test_category.id, name=TEST_NAME, status=TEST_STATUS, privacy=TEST_PRIVACY)

            result = service.create(test_category)

            self.assertEqual(expected, result)

    @patch("services.category_service.get_by_id")
    @patch("services.category_service.update_query")
    def test_changePrivacy_fromPublicToPrivate(self, mock_update_query, mock_get_by_id):
        test_category = create_category(2)
        mock_get_by_id.return_value = test_category
        result = service.change_privacy(2)

        mock_update_query.assert_called_once_with("update categories set is_private = 1 where id = ?", (2,))
        self.assertEqual("private", result.privacy)

    @patch("services.category_service.get_by_id")
    @patch("services.category_service.update_query")
    def test_changePrivacy_fromPrivateToPublic(self, mock_update_query, mock_get_by_id):
        test_category = create_category(2)
        test_category.privacy = "private"
        mock_get_by_id.return_value = test_category
        result = service.change_privacy(2)

        mock_update_query.assert_called_once_with("update categories set is_private = 0 where id = ?", (2,))
        self.assertEqual("public", result.privacy)


    @patch("services.category_service.get_by_id")
    @patch("services.category_service.update_query")
    def test_changeAccessibility_fromUnlockedToLocked(self, mock_update_query, mock_get_by_id):
        test_category = create_category(2)
        mock_get_by_id.return_value = test_category
        result = service.change_accessibility(2)

        mock_update_query.assert_called_once_with("update categories set is_locked = 1 where id = ?", (2,))
        self.assertEqual("locked", result.status)

    @patch("services.category_service.get_by_id")
    @patch("services.category_service.update_query")
    def test_changeAccessibility_fromLockedToUnlocked(self, mock_update_query, mock_get_by_id):
        test_category = create_category(2)
        test_category.status = "locked"
        mock_get_by_id.return_value = test_category
        result = service.change_accessibility(2)

        mock_update_query.assert_called_once_with("update categories set is_locked = 0 where id = ?", (2,))
        self.assertEqual("unlocked", result.status)

