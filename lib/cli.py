import click
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, Coffee, Ingredient, Order, OrderItem, Inventory
from lib.db.init_db import engine
from lib.helpers import format_price, get_coffee_by_id, get_ingredient_by_id

Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """Coffee Shop CLI - Manage your coffee shop operations."""
    pass

@cli.command()
def menu():
    """Display the coffee menu."""
    session = Session()
    try:
        coffees = session.query(Coffee).all()
        click.echo("\n☕ Coffee Menu:")
        click.echo("=" * 50)
        for coffee in coffees:
            click.echo(f"{coffee.id:2d}. {coffee.name:20} {format_price(coffee.price)}")
        click.echo()
    finally:
        session.close()

@cli.command()
@click.argument('coffee_id', type=int)
@click.argument('quantity', type=int, default=1)
def order(coffee_id, quantity):
    """Place an order for coffee."""
    session = Session()
    try:
        coffee = get_coffee_by_id(session, coffee_id)
        if not coffee:
            click.echo(f"Error: Coffee with ID {coffee_id} not found.")
            return

        # Check inventory
        can_make = True
        missing_ingredients = []
        
        for ingredient_usage in coffee.ingredients:
            inventory = session.query(Inventory).filter_by(
                ingredient_id=ingredient_usage.ingredient_id
            ).first()
            
            required_amount = ingredient_usage.quantity * quantity
            if not inventory or inventory.quantity < required_amount:
                can_make = False
                ingredient = get_ingredient_by_id(session, ingredient_usage.ingredient_id)
                missing_ingredients.append(
                    f"{ingredient.name} (need {required_amount}, have {inventory.quantity if inventory else 0})"
                )

        if not can_make:
            click.echo("Cannot fulfill order. Missing ingredients:")
            for missing in missing_ingredients:
                click.echo(f"  - {missing}")
            return

        # Create order
        new_order = Order(total_price=coffee.price * quantity)
        session.add(new_order)
        session.flush()  # Get the order ID

        # Add order item
        order_item = OrderItem(
            order_id=new_order.id,
            coffee_id=coffee.id,
            quantity=quantity,
            price=coffee.price
        )
        session.add(order_item)

        # Update inventory
        for ingredient_usage in coffee.ingredients:
            inventory = session.query(Inventory).filter_by(
                ingredient_id=ingredient_usage.ingredient_id
            ).first()
            inventory.quantity -= ingredient_usage.quantity * quantity

        session.commit()
        
        click.echo(f"✅ Order placed successfully!")
        click.echo(f"   Coffee: {coffee.name}")
        click.echo(f"   Quantity: {quantity}")
        click.echo(f"   Total: {format_price(new_order.total_price)}")
        
    except Exception as e:
        session.rollback()
        click.echo(f"Error placing order: {e}")
    finally:
        session.close()

@cli.command()
def inventory():
    """Check current inventory levels."""
    session = Session()
    try:
        inventory_items = session.query(Inventory).join(Inventory.ingredient).all()
        
        click.echo("\n📦 Inventory:")
        click.echo("=" * 50)
        for item in inventory_items:
            status = "✅" if item.quantity > 10 else "⚠️ " if item.quantity > 0 else "❌"
            # Use general format that works for both int and float
            click.echo(f"{status} {item.ingredient.name:15} {item.quantity:6.1f} {item.ingredient.unit}")
        click.echo()
        
    finally:
        session.close()

@cli.command()
@click.option('--days', default=7, help='Number of days to include in report')
def report(days):
    """Generate sales report."""
    session = Session()
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Total sales
        total_sales = session.query(func.sum(Order.total_price)).filter(
            Order.created_at >= start_date
        ).scalar() or 0
        
        # Number of orders
        order_count = session.query(Order).filter(
            Order.created_at >= start_date
        ).count()
        
        # Popular coffees
        popular_coffees = session.query(
            Coffee.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
        ).join(OrderItem.coffee).join(OrderItem.order).filter(
            Order.created_at >= start_date
        ).group_by(Coffee.id).order_by(func.sum(OrderItem.quantity).desc()).all()
        
        click.echo(f"\n📊 Sales Report (Last {days} days):")
        click.echo("=" * 60)
        click.echo(f"Total Sales: {format_price(total_sales)}")
        click.echo(f"Number of Orders: {order_count}")
        click.echo(f"Average Order Value: {format_price(total_sales / order_count if order_count > 0 else 0)}")
        
        click.echo("\n🍵 Popular Coffees:")
        for coffee in popular_coffees[:5]:
            click.echo(f"  {coffee.name:15} {coffee.total_quantity:3d} orders, {format_price(coffee.total_revenue)}")
        
        click.echo()
        
    finally:
        session.close()

if __name__ == '__main__':
    cli()