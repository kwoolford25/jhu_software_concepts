Examples
========

Example 1: Basic Order
---------------------

.. code-block:: python

    from src.order import Order

    # Create a new order
    order = Order()
    
    # Add a simple pizza
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    
    # Display the order
    print(order)
    
    # Output:
    # Your order:
    # 1. Thin crust pizza with marinara sauce, mozzarella cheese, and pepperoni. Cost: $9
    #
    # Total cost: $9 (NOT PAID)

Example 2: Multiple Pizzas
-------------------------

.. code-block:: python

    from src.order import Order

    # Create a new order
    order = Order()
    
    # Add first pizza
    order.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
    
    # Add second pizza
    order.input_pizza("thick", ["marinara"], "mozzarella", ["mushrooms"])
    
    # Display the order
    print(order)
    
    # Output:
    # Your order:
    # 1. Thin crust pizza with pesto sauce, mozzarella cheese, and mushrooms. Cost: $11
    # 2. Thick crust pizza with marinara sauce, mozzarella cheese, and mushrooms. Cost: $11
    #
    # Total cost: $22 (NOT PAID)

Example 3: Complex Order
----------------------

.. code-block:: python

    from src.order import Order

    # Create a new order
    order = Order()
    
    # Add a pizza with multiple sauces and toppings
    order.input_pizza(
        "thin", 
        ["liv_sauce", "pesto"], 
        "mozzarella", 
        ["mushrooms", "pepperoni"]
    )
    
    # Display the order
    print(order)
    
    # Mark as paid
    order.order_paid()
    print(order)
    
    # Output after payment:
    # Your order:
    # 1. Thin crust pizza with liv_sauce, pesto sauce, mozzarella cheese, and mushrooms, pepperoni. Cost: $18
    #
    # Total cost: $18 (PAID)