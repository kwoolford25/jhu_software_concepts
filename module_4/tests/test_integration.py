import pytest

@pytest.mark.order
@pytest.mark.pizza
def test_multiple_pizzas():
    """Test that an order can contain multiple pizzas with correct cost calculation."""
    order = Order()
    
    # Add first pizza: Thin ($5) + Pesto ($3) + Mozzarella + Mushrooms ($3) = $11
    order.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
    assert order.cost == 11
    
    # Add second pizza: Thick ($6) + Marinara ($2) + Mozzarella + Mushrooms ($3) = $11
    order.input_pizza("thick", ["marinara"], "mozzarella", ["mushrooms"])
    assert order.cost == 22  # Total should be $11 + $11 = $22
    
    # Verify order has two pizzas
    assert len(order.pizzas) == 2

@pytest.mark.order
@pytest.mark.pizza
def test_complex_order():
    """Test a complex order with multiple pizzas and multiple toppings/sauces."""
    order = Order()
    
    # Order 1 from assignment:
    # Pizza 1: Thin ($5) + Pesto ($3) + Mozzarella + Mushrooms ($3) = $11
    order.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
    
    # Pizza 2: Thick ($6) + Marinara ($2) + Mozzarella + Mushrooms ($3) = $11
    order.input_pizza("thick", ["marinara"], "mozzarella", ["mushrooms"])
    
    assert order.cost == 22
    
    # Create a new order
    order2 = Order()
    
    # Order 2 from assignment:
    # Pizza 1: Gluten Free ($8) + Marinara ($2) + Mozzarella + Pineapple ($1) = $11
    order2.input_pizza("gluten_free", ["marinara"], "mozzarella", ["pineapple"])
    
    # Pizza 2: Thin ($5) + Liv Sauce ($5) + Pesto ($3) + Mozzarella + Mushrooms ($3) + Pepperoni ($2) = $18
    order2.input_pizza("thin", ["liv_sauce", "pesto"], "mozzarella", ["mushrooms", "pepperoni"])
    
    assert order2.cost == 29