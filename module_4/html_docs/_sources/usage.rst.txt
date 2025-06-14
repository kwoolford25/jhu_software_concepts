Usage
=====

Basic Usage
----------

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

Crusts
^^^^^^

.. list-table::
   :header-rows: 1

   * - Crust Type
     - Cost
   * - thin
     - $5
   * - thick
     - $6
   * - gluten_free
     - $8

Sauces
^^^^^^

.. list-table::
   :header-rows: 1

   * - Sauce Type
     - Cost
   * - marinara
     - $2
   * - pesto
     - $3
   * - liv_sauce
     - $5

Toppings
^^^^^^^

.. list-table::
   :header-rows: 1

   * - Topping Type
     - Cost
   * - pineapple
     - $1
   * - pepperoni
     - $2
   * - mushrooms
     - $3

Cheese
^^^^^^

Only mozzarella cheese is supported (included in the base price).

Rules
-----

1. Each pizza must include at least one sauce and one topping
2. Only one crust option is allowed per pizza
3. Multiple sauces and toppings are allowed
4. The total cost is calculated by adding the costs of all ingredients