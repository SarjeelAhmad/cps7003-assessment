from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Ideally hashed
    email = Column(String, nullable=False, unique=True)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text)

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    items_sold = Column(Text)

# Relationships (optional, for advanced queries)
User.expenses = relationship('Expense', backref='user')
User.sales = relationship('Sale', backref='user')
