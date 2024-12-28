# test_expense_management.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import Base, Expense, User
from business_logic.expense_management import create_expense, get_expenses, update_expense, delete_expense
from business_logic.user_management import create_user


class TestExpenseManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.Session()
        self.user = create_user(self.db, 'testuser', 'password123', 'testuser@example.com')

    def tearDown(self):
        self.db.close()

    def test_create_expense(self):
        expense = create_expense(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 100.0, 'Food', 'Lunch', self.user.id)
        self.assertIsNotNone(expense.id)

    def test_get_expenses(self):
        create_expense(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 100.0, 'Food', 'Lunch', self.user.id)
        expenses = get_expenses(self.db, self.user.id)
        self.assertEqual(len(expenses), 1)

    def test_update_expense(self):
        expense = create_expense(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 100.0, 'Food', 'Lunch', self.user.id)
        updated_expense = update_expense(self.db, expense.id, amount=150.0)
        self.assertEqual(updated_expense.amount, 150.0)

    def test_delete_expense(self):
        expense = create_expense(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 100.0, 'Food', 'Lunch', self.user.id)
        delete_expense(self.db, expense.id)
        expenses = get_expenses(self.db, self.user.id)
        self.assertEqual(len(expenses), 0)


if __name__ == '__main__':
    unittest.main()