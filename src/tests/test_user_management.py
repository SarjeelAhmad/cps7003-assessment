# test_user_management.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User
from business_logic.user_management import create_user, get_user, update_user, delete_user
from database.models import Base


class TestUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_create_user(self):
        user = create_user(self.db, 'testuser', 'password123', 'testuser@example.com')
        self.assertIsNotNone(user.id)

    def test_get_user(self):
        user = create_user(self.db, 'testuser2', 'password123', 'testuser2@example.com')
        retrieved_user = get_user(self.db, user.id)
        self.assertEqual(user.username, retrieved_user.username)

    def test_update_user(self):
        user = create_user(self.db, 'testuser3', 'password123', 'testuser3@example.com')
        updated_user = update_user(self.db, user.id, username='updateduser')
        self.assertEqual(updated_user.username, 'updateduser')

    def test_delete_user(self):
        user = create_user(self.db, 'testuser4', 'password123', 'testuser4@example.com')
        delete_user(self.db, user.id)
        deleted_user = get_user(self.db, user.id)
        self.assertIsNone(deleted_user)


if __name__ == '__main__':
    unittest.main()