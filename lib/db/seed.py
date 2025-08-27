"""
Database seeding script for coffee shop CLI.
"""

from sqlalchemy.orm import sessionmaker
from lib.db.init_db import engine
from lib.db.models import Coffee, Ingredient, CoffeeIngredient, Inventory, OrderItem, Order

Session = sessionmaker(bind=engine)

def seed_database():
    """Seed the database with initial data."""
    session = Session()
    
    try:
        # Clear existing data (in correct order to respect foreign key constraints)
        session.query(Inventory).delete()
        session.query(CoffeeIngredient).delete()
        session.query(OrderItem).delete()
        session.query(Order).delete()
        session.query(Coffee).delete()
        session.query(Ingredient).delete()
        
        # Create ingredients
        ingredients_data = [
            {"name": "Coffee Beans", "unit": "g", "initial_quantity": 5000},
            {"name": "Milk", "unit": "ml", "initial_quantity": 10000},
            {"name": "Sugar", "unit": "g", "initial_quantity": 2000},
            {"name": "Chocolate Syrup", "unit": "ml", "initial_quantity": 2000},
            {"name": "Whipped Cream", "unit": "g", "initial_quantity": 1000},
            {"name": "Vanilla Syrup", "unit": "ml", "initial_quantity": 1500},
            {"name": "Caramel Syrup", "unit": "ml", "initial_quantity": 1500},
            {"name": "Ice", "unit": "g", "initial_quantity": 20000},
            {"name": "Water", "unit": "ml", "initial_quantity": 50000},  # Added water
        ]
        
        ingredients = {}
        for data in ingredients_data:
            ingredient = Ingredient(name=data["name"], unit=data["unit"])
            session.add(ingredient)
            session.flush()  # Get the ID
            
            # Create inventory
            inventory = Inventory(
                ingredient_id=ingredient.id,
                quantity=data["initial_quantity"]
            )
            session.add(inventory)
            
            ingredients[data["name"]] = ingredient
        
        # Create coffees
        coffees_data = [
            {
                "name": "Espresso",
                "price": 2.50,
                "ingredients": [
                    {"name": "Coffee Beans", "quantity": 18},
                ]
            },
            {
                "name": "Americano",
                "price": 3.00,
                "ingredients": [
                    {"name": "Coffee Beans", "quantity": 18},
                    {"name": "Water", "quantity": 250},
                ]
            },
            {
                "name": "Latte",
                "price": 4.50,
                "ingredients": [
                    {"name": "Coffee Beans", "quantity": 18},
                    {"name": "Milk", "quantity": 250},
                ]
            },
            {
                "name": "Cappuccino",
                "price": 4.00,
                "ingredients": [
                    {"name": "Coffee Beans", "quantity": 18},
                    {"name": "Milk", "quantity": 150},
                ]
            },
            {
                "name": "Mocha",
                "price": 5.00,
                "ingredients": [
                    {"name": "Coffee Beans", "quantity": 18},
                    {"name": "Milk", "quantity": 200},
                    {"name": "Chocolate Syrup", "quantity": 30},
                ]
            },
            {
                "name": "Iced Coffee",
                "price": 4.00,
                "ingredients": [
                    {"name": "Coffee Beans", "quantity": 18},
                    {"name": "Ice", "quantity": 200},
                    {"name": "Milk", "quantity": 100},
                    {"name": "Sugar", "quantity": 10},
                ]
            },
        ]
        
        for data in coffees_data:
            coffee = Coffee(name=data["name"], price=data["price"])
            session.add(coffee)
            session.flush()  # Get the ID
            
            # Add ingredients
            for ing_data in data["ingredients"]:
                if ing_data["name"] in ingredients:
                    coffee_ingredient = CoffeeIngredient(
                        coffee_id=coffee.id,
                        ingredient_id=ingredients[ing_data["name"]].id,
                        quantity=ing_data["quantity"]
                    )
                    session.add(coffee_ingredient)
        
        session.commit()
        print("Database seeded successfully!")
        print(f"Created {len(coffees_data)} coffees and {len(ingredients_data)} ingredients.")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    seed_database()