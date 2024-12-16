from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dal.models import Base
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/database.db')


def initialize_database():
    # Connect to SQLite database
    engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)

    # Create tables based on SQLAlchemy models
    Base.metadata.create_all(engine)

    # Populate database with initial data if it exists
    init_data_path = os.path.join(os.path.dirname(__file__), '../../data/init_data.sql')
    if os.path.exists(init_data_path):
        with engine.connect() as connection, open(init_data_path, 'r') as f:
            sql_script = f.read()
            connection.execute(sql_script)


if __name__ == "__main__":
    initialize_database()
