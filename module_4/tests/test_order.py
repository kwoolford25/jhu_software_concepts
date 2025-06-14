import pytest
from src.order import Order

@pytest.mark.order
def test_order_init():
    """Test order initialization."""
    order = Order()
    assert hasattr(order, 'pizzas')
    assert len(order.pizzas) == 0
    assert order.cost == 0
    assert not hasattr(order, 'paid') or not order.paid

@pytest.mark.order
def test_order_str():
    """Test order string representation."""
    order = Order()
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    order_str = str(order)
    assert "thin" in order_str.lower()
    assert "marinara" in order_str.lower()
    assert "mozzarella" in order_str.lower()
    assert "pepperoni" in order_str.lower()
    assert str(order.cost) in order_str

@pytest.mark.order
def test_order_input_pizza():
    """Test adding a pizza to an order."""
    order = Order()
    initial_cost = order.cost
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    assert len(order.pizzas) == 1
    assert order.cost > initial_cost
    assert order.cost == 9  # Thin ($5) + Marinara ($2) + Pepperoni ($2) = $9

@pytest.mark.order
def test_order_paid():
    """Test marking an order as paid."""
    order = Order()
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    order.order_paid()
    assert hasattr(order, 'paid')
    assert order.paid