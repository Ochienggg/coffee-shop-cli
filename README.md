# Coffee Shop CLI

A command-line interface application for managing a coffee shop's operations, built with Python, SQLAlchemy, and Click. Track inventory, process orders, and generate sales reports - all from your terminal!

## Features

- **Menu Management**: Display available coffee drinks with prices
- **Order Processing**: Place orders with real-time inventory validation
- **Inventory Tracking**: Monitor ingredient levels with visual status indicators
- **Sales Reporting**: Generate detailed sales reports with popular item analytics
- **Database Persistence**: SQLite database with proper schema migrations
- **Interactive CLI**: User-friendly command-line interface with helpful feedback

## Architecture
coffee_shop_cli/
├── lib/ # Main application code
│ ├── cli.py # Click command-line interface
│ ├── debug.py # Development debugging tools
│ ├── helpers.py # Utility functions
│ └── db/ # Database layer
│ ├── models.py # SQLAlchemy ORM models
│ ├── init_db.py # Database initialization
│ ├── seed.py # Sample data seeding
│ └── migrations/ # Alembic database migrations
├── tests/ # Test suite
└── coffee_shop.db # SQLite database (created automatically)

text

## Quick Start

### Prerequisites

- Python 3.9+
- pipenv (install with `pip install pipenv`)

### Installation & Setup

1. **Clone and navigate to the project**:
   ```bash
   git clone <your-repo-url>
   cd coffee-shop-cli
Install dependencies:

bash
pipenv install
pipenv install --dev  # Development dependencies
Initialize the database:

bash
pipenv run python -m lib.db.init_db
Seed with sample data:

bash
pipenv run python -m lib.db.seed
Run the application:

bash
pipenv run python -m lib.cli
Usage Guide
Interactive Mode
Start the interactive CLI session:

bash
pipenv run python -m lib.cli
Direct Commands
Run commands directly without entering interactive mode:

bash
pipenv run python -m lib.cli menu
pipenv run python -m lib.cli order 3 2
pipenv run python -m lib.cli inventory
pipenv run python -m lib.cli report --days 7
Available Commands
Display Menu
bash
> menu
Shows all available coffee drinks with IDs, names, and prices.

Check Inventory
bash
> inventory
Displays current ingredient levels with visual status indicators:

Good stock (>10 units)

Low stock (1-10 units)

Out of stock (0 units)

Place an Order
bash
> order <coffee_id> <quantity>
Examples:

bash
> order 1 1    # 1 Espresso
> order 3 2    # 2 Lattes
> order 6 1    # 1 Iced Coffee
The system validates inventory in real-time and prevents orders that can't be fulfilled.

Generate Sales Report
bash
> report [--days DAYS]
Examples:

bash
> report          # Last 7 days (default)
> report --days 3 # Last 3 days
Shows:

Total sales revenue

Number of orders

Average order value

Most popular coffee drinks

Sample Workflow
bash
# See what's available
$ pipenv run python -m lib.cli menu

Coffee Menu:
==================================================
 1. Espresso              $2.50
 2. Americano             $3.00
 3. Latte                 $4.50
 4. Cappuccino            $4.00
 5. Mocha                 $5.00
 6. Iced Coffee           $4.00

# Place an order for 2 Lattes
$ pipenv run python -m lib.cli order 3 2

Order placed successfully!
   Coffee: Latte
   Quantity: 2
   Total: $9.00

# Check updated inventory
$ pipenv run python -m lib.cli inventory

 Inventory:
==================================================
Coffee Beans      4964 g
Milk              9500 ml
Sugar             2000 g
Chocolate Syrup   2000 ml
 Whipped Cream     1000 g
Vanilla Syrup     1500 ml
Caramel Syrup     1500 ml
Ice               20000 g
Water             50000 ml

# Generate sales report
$ pipenv run python -m lib.cli report

Sales Report (Last 7 days):
============================================================
Total Sales: $9.00
Number of Orders: 1
Average Order Value: $9.00

Popular Coffees:
  Latte            2 orders, $9.00
 Development
Running Tests
bash
pipenv run pytest
Debug Tools
bash
# Show detailed menu information
pipenv run python -m lib.debug menu

# Show inventory details
pipenv run python -m lib.debug inventory

# Show order history
pipenv run python -m lib.debug orders

# Reset database and reseed
pipenv run python -m lib.debug reset
Database Management
Initialize fresh database:

bash
pipenv run python -m lib.db.init_db
pipenv run python -m lib.db.seed
Run migrations (when schema changes):

bash
pipenv run alembic upgrade head

The application uses these main entities:

Coffee: Drink definitions (Espresso, Latte, etc.)

Ingredient: Raw materials (Coffee Beans, Milk, etc.)

CoffeeIngredient: Recipe mapping (how much of each ingredient per drink)

Inventory: Current stock levels

Order: Customer transactions

OrderItem: Individual items within orders

Troubleshooting
Database issues:

bash
# Reset everything
rm coffee_shop.db
pipenv run python -m lib.db.init_db
pipenv run python -m lib.db.seed
Dependency issues:

bash
# Reinstall dependencies
pipenv --rm
pipenv install
pipenv shell
