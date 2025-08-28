# lib/models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    orders = relationship("Order", back_populates="customer")

class MenuItem(Base):
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    category = Column(String)
    
    order_items = relationship("OrderItem", back_populates="menu_item")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Numeric(10, 2))
    status = Column(String, default='pending')
    
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), primary_key=True)
    quantity = Column(Integer)
    price_at_time = Column(Numeric(10, 2))
    
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")

# Database setup
engine = create_engine('sqlite:///coffee_shop.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()