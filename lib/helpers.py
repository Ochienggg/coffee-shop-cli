"""
Helper functions for coffee shop CLI.
"""

from sqlalchemy.orm import Session
from lib.db.models import Coffee, Ingredient, Inventory

def format_price(price):
    """Format price as currency."""
    return f"${price:.2f}"

def get_coffee_by_id(session: Session, coffee_id: int):
    """Get coffee by ID."""
    return session.query(Coffee).filter_by(id=coffee_id).first()

def get_ingredient_by_id(session: Session, ingredient_id: int):
    """Get ingredient by ID."""
    return session.query(Ingredient).filter_by(id=ingredient_id).first()

def calculate_order_total(coffee, quantity):
    """Calculate total price for an order."""
    return coffee.price * quantity

def check_inventory(session: Session, coffee, quantity):
    """Check if there's enough inventory to make coffee."""
    for ingredient_usage in coffee.ingredients:
        inventory = session.query(Inventory).filter_by(
            ingredient_id=ingredient_usage.ingredient_id
        ).first()
        
        required = ingredient_usage.quantity * quantity
        if not inventory or inventory.quantity < required:
            return False, ingredient_usage.ingredient
    
    return True, None

def update_inventory(session: Session, coffee, quantity):
    """Update inventory after making coffee."""
    for ingredient_usage in coffee.ingredients:
        inventory = session.query(Inventory).filter_by(
            ingredient_id=ingredient_usage.ingredient_id
        ).first()
        
        if inventory:
            inventory.quantity -= ingredient_usage.quantity * quantity