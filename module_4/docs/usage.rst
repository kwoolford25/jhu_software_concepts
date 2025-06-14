Usage
=====

Creating a Basic Order
---------------------

Here's how to create a basic pizza order:

.. code-block:: python

    from src.order import Order

    # Create a new order
    order = Order()

    # Add a pizza to the order
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])

    # Display the order
    print(order)

    # Mark the order as paid
    order.order_paid()

Pizza Options
------------

The system supports the following options:

Crusts:
  - thin ($5)
  - thick ($6)
  - gluten_free ($8)

Sauces:
  - marinara ($2)
  - pesto ($3)
  - liv_sauce ($5)

Toppings:
  - pineapple ($1)
  - pepperoni ($2)
  - mushrooms ($3)

Cheese:
  - mozzarella (included)

Example Orders
-------------

Example Order 1:
  - Pizza with thin crust, pesto sauce, mozzarella cheese, and mushrooms
  - Pizza with thick crust, marinara sauce, mozzarella cheese, and mushrooms

Example Order 2:
  - Pizza with gluten-free crust, marinara sauce, mozzarella cheese, and pineapple
  - Pizza with thin crust, liv sauce and pesto sauce, mozzarella cheese, mushrooms, and pepperoni