#!/usr/bin/env python3
"""
Debug script for coffee shop CLI development.
"""

import sys
from sqlalchemy.orm import sessionmaker
from lib.db.init_db import engine, init_database
from lib.db.models import Base, Coffee, Ingredient, Order, OrderItem, Inventory, CoffeeIngredient
from lib.db.seed import seed_database

Session = sessionmaker(bind=engine)

def debug_menu():
    """Debug menu functionality."""
    session = Session()
    try:
        print("\n=== DEBUG: Coffee Menu ===")
        coffees = session.query(Coffee).all()
        for coffee in coffees:
            print(f"{coffee.id}: {coffee.name} - ${coffee.price:.2f}")
            for ingredient in coffee.ingredients:
                print(f"  - {ingredient.ingredient.name}: {ingredient.quantity} {ingredient.ingredient.unit}")
    finally:
        session.close()

def debug_inventory():
    """Debug inventory functionality."""
    session = Session()
    try:
        print("\n=== DEBUG: Inventory ===")
        inventory = session.query(Inventory).join(Inventory.ingredient).all()
        for item in inventory:
            print(f"{item.ingredient.name}: {item.quantity} {item.ingredient.unit}")
    finally:
        session.close()

def debug_orders():
    """Debug orders functionality."""
    session = Session()
    try:
        print("\n=== DEBUG: Orders ===")
        orders = session.query(Order).all()
        for order in orders:
            print(f"Order #{order.id}: ${order.total_price:.2f} - {order.created_at}")
            for item in order.items:
                print(f"  - {item.coffee.name} x{item.quantity}")
    finally:
        session.close()

def debug_reset():
    """Reset and seed the database."""
    print("\n=== DEBUG: Resetting Database ===")
    init_database()
    seed_database()
    print("Database reset and seeded successfully!")

def main():
    """Main debug function."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'menu':
            debug_menu()
        elif command == 'inventory':
            debug_inventory()
        elif command == 'orders':
            debug_orders()
        elif command == 'reset':
            debug_reset()
        else:
            print(f"Unknown command: {command}")
    else:
        print("""
Coffee Shop CLI Debug Tools

Usage:
  python -m lib.debug <command>

Commands:
  menu       - Show coffee menu details
  inventory  - Show inventory details
  orders     - Show order details
  reset      - Reset and seed database
        """)

if __name__ == '__main__':
    main()