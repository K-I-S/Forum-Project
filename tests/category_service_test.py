import unittest
from unittest.mock import Mock, patch
from data.models import Category, UserAccess, PrivilegedUserView
from services import category_service as service

TEST_NAME = "Test Category"
TEST_STATUS = "unlocked"
TEST_PRIVACY = "public"
TEST_DESCRIPTION = "test description"
CATEGORIES_ID = 1
USERS_ID = 2



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

def fake_access():
    return UserAccess.from_query_result(
        categories_id = CATEGORIES_ID,
        users_id=USERS_ID,
        access_type="read")

def fake_privileged_user(id, access_type):
    return PrivilegedUserView.from_query_result(
        id=id,
        access_type=access_type)

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

        mock_update_query.assert_called_with("update topics set is_locked = 1 where category_id = ?", (2,))
        self.assertEqual("locked", result.status)

    @patch("services.category_service.get_by_id")
    @patch("services.category_service.update_query")
    def test_changeAccessibility_fromLockedToUnlocked(self, mock_update_query, mock_get_by_id):
        test_category = create_category(2)
        test_category.status = "locked"
        mock_get_by_id.return_value = test_category
        result = service.change_accessibility(2)

        mock_update_query.assert_called_with("update categories set is_locked = 0 where id = ?", (2,))
        self.assertEqual("unlocked", result.status)

    @patch("services.category_service.read_query")
    def test_checkForAccess_returnsCorrectUserAccess(self, mock_read_query):
        mock_read_query.return_value = [(CATEGORIES_ID, USERS_ID, "read")]

        expected = fake_access()

        result = service.check_for_access(CATEGORIES_ID, USERS_ID)

        mock_read_query.assert_called_once_with(
            "select categories_id, users_id, access_type from categories_access where categories_id = ? and users_id = ?",
            (1, 2))
        self.assertEqual(expected, result)


    @patch("services.category_service.read_query")
    def test_checkForAccess_returnsNoneWhenUserNotFound(self, mock_read_query):
        mock_read_query.return_value = []


        result = service.check_for_access(CATEGORIES_ID, USERS_ID)
        mock_read_query.assert_called_once_with(
            "select categories_id, users_id, access_type from categories_access where categories_id = ? and users_id = ?",
            (1, 2))
        self.assertIsNone(result)

    @patch("services.category_service.check_for_access")
    @patch("services.category_service.insert_query")
    def test_giveUserAccess_givesWriteAccessWhenNoPreviousAccess(self, mock_insert_query, mock_check_for_access):
        mock_check_for_access.return_value = None

        result = service.give_user_access(CATEGORIES_ID, USERS_ID)

        mock_insert_query.assert_called_once_with(
            "insert into categories_access (categories_id, users_id, access_type) values (?,?,?)", (1, 2, 1))

        self.assertEqual("User 2 has been granted write access!", result)

    @patch("services.category_service.check_for_access")
    @patch("services.category_service.insert_query")
    def test_giveUserAccess_givesReadAccessWhenNoPreviousAccess(self, mock_insert_query, mock_check_for_access):
        mock_check_for_access.return_value = None

        result = service.give_user_access(CATEGORIES_ID, USERS_ID, "read")


        mock_insert_query.assert_called_once_with(
            "insert into categories_access (categories_id, users_id, access_type) values (?,?,?)", (1, 2, 0))

        self.assertEqual("User 2 has been granted read access!", result)

    @patch("services.category_service.check_for_access")
    @patch("services.category_service.insert_query")
    @patch("services.category_service.update_query")
    def test_giveUserAccess_givesReadAccessWhenNoPreviousAccess(self, mock_update_query, mock_insert_query, mock_check_for_access):
        mock_check_for_access.return_value = None

        result = service.give_user_access(CATEGORIES_ID, USERS_ID, "invalid")
        mock_insert_query.assert_not_called()
        mock_update_query.assert_not_called()

        self.assertEqual("Invalid access_type: please choose between read and write!", result)



    @patch("services.category_service.check_for_access")
    @patch("services.category_service.insert_query")
    @patch("services.category_service.update_query")
    def test_giveUserAccess_givesReadAccessWhenNoPreviousAccess(self, mock_update_query, mock_insert_query, mock_check_for_access):
        mock_check_for_access.return_value = 1

        result = service.give_user_access(CATEGORIES_ID, USERS_ID, "read")
        mock_update_query.assert_called_once_with(
            "update categories_access set access_type = ? where categories_id = ? and users_id = ?", ( 0, 1, 2))

        self.assertEqual("User 2 has been granted read access!", result)

    @patch("services.category_service.check_for_access")
    @patch("services.category_service.update_query")
    def test_revokeUserAccess_revokesAccessToUser(self, mock_update_query, mock_check_for_access):
        mock_check_for_access.return_value = 1


        result = service.revoke_user_access(CATEGORIES_ID, USERS_ID)
        mock_update_query.assert_called_once_with("delete from categories_access where categories_id = ? and users_id = ?", (1, 2))

        self.assertEqual("The access of user with ID 2 has been successfully revoked", result)

    @patch("services.category_service.check_for_access")
    @patch("services.category_service.update_query")
    def test_revokeUserAccess_returnsMessageWhenUserDoestHaveAccess(self, mock_update_query, mock_check_for_access):
        mock_check_for_access.return_value = None


        result = service.revoke_user_access(CATEGORIES_ID, USERS_ID)
        mock_update_query.assert_not_called()

        self.assertEqual("The user does not have access to this category!", result)

    @patch("services.category_service.read_query")
    def test_userHasReadAccess_returnsTrueWhenHasAccess(self, mock_read_query):
        mock_read_query.return_value = [(CATEGORIES_ID, USERS_ID, "read")]

        result = service.user_has_read_access(CATEGORIES_ID, USERS_ID)

        self.assertTrue(result)

    @patch("services.category_service.read_query")
    def test_userHasReadAccess_returnsFalseWhenDoesntHaveAccess(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.user_has_read_access(CATEGORIES_ID, USERS_ID)

        self.assertFalse(result)

    @patch("services.category_service.read_query")
    def test_userHasWriteAccess_returnsTrueWhenHasAccess(self, mock_read_query):
        mock_read_query.return_value = [(CATEGORIES_ID, USERS_ID, "write")]

        result = service.user_has_write_access(CATEGORIES_ID, USERS_ID)

        self.assertTrue(result)

    @patch("services.category_service.read_query")
    def test_userHasWriteAccess_returnsFalseWhenDoesntHaveAccess(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.user_has_write_access(CATEGORIES_ID, USERS_ID)

        self.assertFalse(result)

    @patch("services.category_service.read_query")
    def test_getPrivileged_returnsAllPrivilegedUsers(self, mock_read_query):
        mock_read_query.return_value = [(1, "read"), (2, "write")]

        result = service.get_privileged(2)
        result = list(result)

        expected = [fake_privileged_user(1, "read"), fake_privileged_user(2, "write")]

        mock_read_query.assert_called_once_with("select users_id, access_type from categories_access where "
                                                "categories_id = ?", (2,))
        self.assertEqual(expected, result)

    @patch("services.category_service.read_query")
    def test_getPrivileged_returnsEmptyListWhenNoPrivilegedUsersFound(self, mock_read_query):
        mock_read_query.return_value = []

        result = service.get_privileged(2)
        result = list(result)

        expected = []

        mock_read_query.assert_called_once_with("select users_id, access_type from categories_access where "
                                                "categories_id = ?", (2,))
        self.assertEqual(expected, result)

