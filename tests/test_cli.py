import pytest
from click.testing import CliRunner
from lib.cli import cli
from lib.db.init_db import init_database
from lib.db.seed import seed_database

@pytest.fixture(scope="module")
def runner():
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Set up test database."""
    init_database()
    seed_database()

def test_menu_command(runner):
    """Test menu command."""
    result = runner.invoke(cli, ['menu'])
    assert result.exit_code == 0
    assert "Coffee Menu" in result.output
    assert "Espresso" in result.output

def test_inventory_command(runner):
    """Test inventory command."""
    result = runner.invoke(cli, ['inventory'])
    assert result.exit_code == 0
    assert "Inventory" in result.output
    assert "Coffee Beans" in result.output

def test_order_command_valid(runner):
    """Test valid order command."""
    # First check inventory to ensure we can make the order
    result = runner.invoke(cli, ['order', '1', '1'])  # Order 1 espresso
    assert result.exit_code == 0
    assert "Order placed successfully" in result.output

def test_order_command_invalid_coffee(runner):
    """Test order command with invalid coffee ID."""
    result = runner.invoke(cli, ['order', '999', '1'])
    assert result.exit_code == 0
    assert "not found" in result.output

def test_report_command(runner):
    """Test report command."""
    result = runner.invoke(cli, ['report', '--days', '1'])
    assert result.exit_code == 0
    assert "Sales Report" in result.output