import pytest
from sqlalchemy.orm import sessionmaker
from lib.db.init_db import engine, init_database
from lib.db.models import Coffee, Ingredient, Order, OrderItem, Inventory, CoffeeIngredient

Session = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def test_session():
    """Create a test database session."""
    init_database()
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_coffee_creation(test_session):
    """Test creating a coffee."""
    coffee = Coffee(name="Test Coffee", price=3.50)
    test_session.add(coffee)
    test_session.commit()
    
    retrieved = test_session.query(Coffee).filter_by(name="Test Coffee").first()
    assert retrieved is not None
    assert retrieved.price == 3.50

def test_ingredient_creation(test_session):
    """Test creating an ingredient."""
    ingredient = Ingredient(name="Test Ingredient", unit="g")
    test_session.add(ingredient)
    test_session.commit()
    
    retrieved = test_session.query(Ingredient).filter_by(name="Test Ingredient").first()
    assert retrieved is not None
    assert retrieved.unit == "g"

def test_coffee_ingredient_relationship(test_session):
    """Test coffee-ingredient relationship."""
    # Create coffee and ingredient
    coffee = Coffee(name="Test Coffee", price=3.50)
    ingredient = Ingredient(name="Test Ingredient", unit="g")
    
    test_session.add_all([coffee, ingredient])
    test_session.flush()
    
    # Create relationship
    coffee_ingredient = CoffeeIngredient(
        coffee_id=coffee.id,
        ingredient_id=ingredient.id,
        quantity=10.0
    )
    test_session.add(coffee_ingredient)
    test_session.commit()
    
    # Test relationships
    assert len(coffee.ingredients) == 1
    assert coffee.ingredients[0].ingredient == ingredient
    assert len(ingredient.coffee_associations) == 1
    assert ingredient.coffee_associations[0].coffee == coffee

def test_order_creation(test_session):
    """Test creating an order."""
    order = Order(total_price=10.50)
    test_session.add(order)
    test_session.commit()
    
    retrieved = test_session.query(Order).first()
    assert retrieved is not None
    assert retrieved.total_price == 10.50

def test_inventory_creation(test_session):
    """Test creating inventory."""
    ingredient = Ingredient(name="Test Ingredient", unit="g")
    test_session.add(ingredient)
    test_session.flush()
    
    inventory = Inventory(ingredient_id=ingredient.id, quantity=100.0)
    test_session.add(inventory)
    test_session.commit()
    
    retrieved = test_session.query(Inventory).first()
    assert retrieved is not None
    assert retrieved.quantity == 100.0
    assert retrieved.ingredient == ingredient