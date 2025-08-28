from lib.helpers import *
from lib.models import session

def main_menu():
    current_customer = None

    while True:
        print("\n--- Coffee Shop CLI ---")
        print("1. View menu")
        print("2. Register customer")
        print("3. Select customer")
        if current_customer:
            print(f"4. Place order ({current_customer.name})")
            print("5. View order history")
        print("6. View all orders")
        print("7. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            menu_items = get_all_menu_items()
            if menu_items:
                print("\n--- Menu ---")
                for item in menu_items:
                    print(f"{item.id}. {item.name} - ${item.price} ({item.category})")
                    print(f"   {item.description}")
            else:
                print("No menu items found")

        elif choice == "2":
            name = input("Enter your name: ").strip()
            email = input("Enter your email: ").strip()
            
            if find_customer_by_email(email):
                print("Email already registered!")
            else:
                current_customer = create_customer(name, email)
                print(f"Customer {name} created!")

        elif choice == "3":
            email = input("Enter customer email: ").strip()
            customer = find_customer_by_email(email)
            if customer:
                current_customer = customer
                print(f"Hello {current_customer.name}!")
            else:
                print("Customer not found")

        elif choice == "4" and current_customer:
            menu_items = get_all_menu_items()
            if not menu_items:
                print("No menu items available")
                continue
                
            print("\nAvailable menu items:")
            for item in menu_items:
                print(f"{item.id}. {item.name} - ${item.price}")
            
            try:
                item_id = int(input("Enter menu item ID: "))
                quantity = int(input("Enter quantity: "))
                
                menu_item = find_menu_item_by_id(item_id)
                if not menu_item:
                    print("Invalid menu item ID")
                    continue
                    
                # Create order
                order = create_order(current_customer.id, menu_item.price * quantity)
                
                # Add order item
                create_order_item(order.id, item_id, quantity, menu_item.price)
                
                print(f"Order placed successfully! Total: ${order.total_amount}")
                
            except ValueError:
                print("Please enter valid numbers")

        elif choice == "5" and current_customer:
            orders = get_customer_orders(current_customer.id)
            if orders:
                print(f"\nOrder history for {current_customer.name}:")
                for order in orders:
                    print(f"Order #{order.id} - ${order.total_amount} - {order.order_date}")
                    order_items = get_order_items(order.id)
                    for item in order_items:
                        menu_item = find_menu_item_by_id(item.menu_item_id)
                        print(f"  {item.quantity}x {menu_item.name} @ ${item.price_at_time}")
            else:
                print("No orders found")

        elif choice == "6":
            orders = get_all_orders()
            if orders:
                print("\n--- All Orders ---")
                for order in orders:
                    customer = find_customer_by_id(order.customer_id)
                    print(f"Order #{order.id} - {customer.name} - ${order.total_amount} - {order.status}")
            else:
                print("No orders found")

        elif choice == "7":
            print("Thank you for visiting our coffee shop!")
            session.close()
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()
