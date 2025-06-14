import pytest

@pytest.mark.pizza
def test_pizza_init():
    """Test that pizza initialization works correctly."""
    pizza = Pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    assert pizza.crust == "thin"
    assert "marinara" in pizza.sauce
    assert pizza.cheese == "mozzarella"
    assert "pepperoni" in pizza.toppings
    assert pizza.cost() > 0

@pytest.mark.pizza
def test_pizza_str():
    """Test that pizza string representation works."""
    pizza = Pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    pizza_str = str(pizza)
    assert "thin" in pizza_str.lower()
    assert "marinara" in pizza_str.lower()
    assert "mozzarella" in pizza_str.lower()
    assert "pepperoni" in pizza_str.lower()
    assert str(pizza.cost()) in pizza_str

@pytest.mark.pizza
def test_pizza_cost():
    """Test that pizza cost calculation works correctly."""
    # Thin ($5) + Marinara ($2) + Pepperoni ($2) = $9
    pizza1 = Pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    assert pizza1.cost() == 9

    # Thick ($6) + Pesto ($3) + Mushrooms ($3) = $12
    pizza2 = Pizza("thick", ["pesto"], "mozzarella", ["mushrooms"])
    assert pizza2.cost() == 12

    # Gluten Free ($8) + Liv Sauce ($5) + Pineapple ($1) = $14
    pizza3 = Pizza("gluten_free", ["liv_sauce"], "mozzarella", ["pineapple"])
    assert pizza3.cost() == 14

    # Thin ($5) + Marinara ($2) + Pesto ($3) + Mushrooms ($3) + Pepperoni ($2) = $15
    pizza4 = Pizza("thin", ["marinara", "pesto"], "mozzarella", ["mushrooms", "pepperoni"])
    assert pizza4.cost() == 15