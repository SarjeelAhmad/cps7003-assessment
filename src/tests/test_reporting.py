# test_reporting.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import Base, Expense, Sale, User
from business_logic.reporting import generate_financial_summary
from business_logic.user_management import create_user
from business_logic.expense_management import create_expense
from business_logic.sales_tracking import record_sale


class TestReporting(unittest.TestCase):
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

    def test_generate_financial_summary(self):
        create_expense(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 100.0, 'Food', 'Lunch', self.user.id)
        record_sale(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 150.0, 'Coffee', self.user.id)
        summary = generate_financial_summary(self.db, self.user.id)
        self.assertEqual(summary['total_expenses'], 100.0)
        self.assertEqual(summary['total_sales'], 150.0)
        self.assertEqual(summary['profit'], 50.0)


if __name__ == '__main__':
    unittest.main()