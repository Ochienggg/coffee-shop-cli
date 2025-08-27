"""
Database initialization script for coffee shop CLI.
"""

from sqlalchemy import create_engine
from lib.db.models import Base

# SQLite database URL
DATABASE_URL = "sqlite:///./coffee_shop.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

def init_database():
    """Initialize the database by creating all tables."""
    try:
        Base.metadata.create_all(engine)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def drop_database():
    """Drop all database tables."""
    try:
        Base.metadata.drop_all(engine)
        print("Database dropped successfully!")
    except Exception as e:
        print(f"Error dropping database: {e}")
        raise

if __name__ == '__main__':
    init_database()