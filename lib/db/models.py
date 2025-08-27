from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for coffee ingredients
coffee_ingredient = Table(
    'coffee_ingredient',
    Base.metadata,
    Column('coffee_id', Integer, ForeignKey('coffees.id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True),
    Column('quantity', Float, nullable=False)
)

class Coffee(Base):
    __tablename__ = 'coffees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ingredients = relationship(
        "CoffeeIngredient",
        back_populates="coffee",
        cascade="all, delete-orphan"
    )
    order_items = relationship("OrderItem", back_populates="coffee")
    
    def __repr__(self):
        return f"<Coffee(name='{self.name}', price={self.price})>"

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    unit = Column(String(20), nullable=False)  # e.g., 'g', 'ml', 'pieces'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    coffee_associations = relationship("CoffeeIngredient", back_populates="ingredient")
    inventory = relationship("Inventory", back_populates="ingredient", uselist=False)
    
    def __repr__(self):
        return f"<Ingredient(name='{self.name}', unit='{self.unit}')>"

class CoffeeIngredient(Base):
    __tablename__ = 'coffee_ingredients'
    
    coffee_id = Column(Integer, ForeignKey('coffees.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(Float, nullable=False)
    
    # Relationships
    coffee = relationship("Coffee", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="coffee_associations")
    
    def __repr__(self):
        return f"<CoffeeIngredient(coffee={self.coffee.name}, ingredient={self.ingredient.name}, quantity={self.quantity})>"

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    items = relationship("OrderItem", back_populates="order")
    
    def __repr__(self):
        return f"<Order(total_price={self.total_price}, created_at={self.created_at})>"

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    coffee_id = Column(Integer, ForeignKey('coffees.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # Price at time of order
    
    # Relationships
    order = relationship("Order", back_populates="items")
    coffee = relationship("Coffee", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(coffee={self.coffee.name}, quantity={self.quantity}, price={self.price})>"

class Inventory(Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False, unique=True)
    quantity = Column(Float, nullable=False, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="inventory")
    
    def __repr__(self):
        return f"<Inventory(ingredient={self.ingredient.name}, quantity={self.quantity})>"