import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from lib.models import session, Customer, MenuItem

def seed_database():
    # Create sample customers
    customers = [
        Customer(name="John Doe", email="john@example.com"),
        Customer(name="Jane Smith", email="jane@example.com"),
        Customer(name="Bob Johnson", email="bob@example.com")
    ]
    
    # Create sample menu items
    menu_items = [
        MenuItem(
            name="Espresso",
            description="Strong black coffee made by forcing steam through ground coffee beans",
            price=2.50,
            category="Hot Coffee"
        ),
        MenuItem(
            name="Cappuccino",
            description="Espresso with steamed milk and a deep layer of foam",
            price=3.50,
            category="Hot Coffee"
        ),
        MenuItem(
            name="Latte",
            description="Espresso with steamed milk and a light layer of foam",
            price=4.00,
            category="Hot Coffee"
        ),
        MenuItem(
            name="Iced Coffee",
            description="Chilled coffee served with ice",
            price=3.00,
            category="Cold Coffee"
        ),
        MenuItem(
            name="Muffin",
            description="Freshly baked blueberry muffin",
            price=2.00,
            category="Pastry"
        )
    ]
    
    session.add_all(customers)
    session.add_all(menu_items)
    session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
