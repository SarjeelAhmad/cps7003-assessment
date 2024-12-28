# test_sales_tracking.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import Base, Sale, User
from business_logic.sales_tracking import record_sale, get_sales, update_sale, delete_sale
from business_logic.user_management import create_user


class TestSalesTracking(unittest.TestCase):
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

    def test_record_sale(self):
        # Convert date string to date object
        date = datetime.strptime('2024-12-22', '%Y-%m-%d').date()
        sale = record_sale(self.db, date, 150.0, 'Coffee', self.user.id)

        self.assertIsNotNone(sale.id)
        self.assertEqual(sale.date, date)
        self.assertEqual(sale.amount, 150.0)
        self.assertEqual(sale.items_sold, 'Coffee')
        self.assertEqual(sale.user_id, self.user.id)

    def test_get_sales(self):
        record_sale(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 150.0, 'Coffee', self.user.id)
        sales = get_sales(self.db, self.user.id)
        self.assertEqual(len(sales), 1)

    def test_update_sale(self):
        sale = record_sale(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 150.0, 'Coffee', self.user.id)
        updated_sale = update_sale(self.db, sale.id, amount=200.0)
        self.assertEqual(updated_sale.amount, 200.0)

    def test_delete_sale(self):
        sale = record_sale(self.db, datetime.strptime('2024-12-22', '%Y-%m-%d').date(), 150.0, 'Coffee', self.user.id)
        delete_sale(self.db, sale.id)
        sales = get_sales(self.db, self.user.id)
        self.assertEqual(len(sales), 0)


if __name__ == '__main__':
    unittest.main()