# test_inventory_management.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Inventory
from business_logic.inventory_management import add_inventory_item, get_inventory_items, update_inventory_item, \
    delete_inventory_item


class TestInventoryManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.Session()

    def tearDown(self):
        self.db.close()

    def test_add_inventory_item(self):
        item = add_inventory_item(self.db, 'Coffee Beans', 50, 200.0)
        self.assertIsNotNone(item.id)

    def test_get_inventory_items(self):
        add_inventory_item(self.db, 'Coffee Beans', 50, 200.0)
        items = get_inventory_items(self.db)
        self.assertEqual(len(items), 1)

    def test_update_inventory_item(self):
        item = add_inventory_item(self.db, 'Coffee Beans', 50, 200.0)
        updated_item = update_inventory_item(self.db, item.id, quantity=100)
        self.assertEqual(updated_item.quantity, 100)

    def test_delete_inventory_item(self):
        item = add_inventory_item(self.db, 'Coffee Beans', 50, 200.0)
        delete_inventory_item(self.db, item.id)
        items = get_inventory_items(self.db)
        self.assertEqual(len(items), 0)


if __name__ == '__main__':
    unittest.main()