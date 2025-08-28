


from .models import session, Customer, MenuItem, Order, OrderIte

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

def get_all_menu_items():
    return session.query(MenuItem).all()

def find_customer_by_email(email):
    return session.query(Customer).filter(Customer.email==email).first()

def create_customer(name, email):
    customer=Customer(name=name, email=email)
    session.add(customer)
    session.commit()
    return customer

def find_menu_item_by_id(item_id):
    return session.query(MenuItem).filter(MenuItem.id==item_id).first()

def create_order(customer_id, total_amount):
    order = Order(customer_id=customer_id, total_amount=total_amount)
    session.add(order)
    session.commit()
    return Order

def create_order_item(order_id, menu_item_id, quantity, price):
    order_item = OrderItem(
        order_id=order_id,
        menu_item_id=menu_item_id,
        quantity=quantity,
        price_at_time=price

    )
    session.add(order_item)
    session.commit()
    return order_item

if __name__ == "__main__":
    seed_database()

