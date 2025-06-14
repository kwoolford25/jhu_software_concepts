from src.pizza import Pizza

class Order:
    """
    Order class for managing customer pizza orders.
    
    This class handles the creation and management of customer orders,
    including adding pizzas, calculating total cost, and processing payment.
    
    Attributes:
        pizzas (list): List of Pizza objects in the order
        cost (int): Total cost of the order
        paid (bool): Payment status of the order
        
    Example:
        >>> order = Order()
        >>> order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
        >>> print(order)
        Your order:
        1. Thin crust pizza with marinara sauce, mozzarella cheese, and pepperoni. Cost: $9
        
        Total cost: $9 (NOT PAID)
    """
    
    def __init__(self):
        """
        Initialize a customer order with empty pizza list and zero cost.
        
        The order starts with no pizzas, zero cost, and is marked as not paid.
        
        Example:
            >>> order = Order()
            >>> len(order.pizzas)
            0
            >>> order.cost
            0
            >>> order.paid
            False
        """
        self.pizzas = []
        self.cost = 0
        self.paid = False
    
    def __str__(self):
        """
        Return a string representation of the complete order.
        
        Returns:
            str: Description of all pizzas in the order and total cost
            
        Example:
            >>> order = Order()
            >>> order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
            >>> print(order)
            Your order:
            1. Thin crust pizza with marinara sauce, mozzarella cheese, and pepperoni. Cost: $9
            
            Total cost: $9 (NOT PAID)
        """
        if not self.pizzas:
            return "Empty order. Total: $0"
        
        order_str = "Your order:\n"
        for i, pizza in enumerate(self.pizzas, 1):
            order_str += f"{i}. {str(pizza)}\n"
        
        order_str += f"\nTotal cost: ${self.cost}"
        if self.paid:
            order_str += " (PAID)"
        else:
            order_str += " (NOT PAID)"
            
        return order_str
    
    def input_pizza(self, crust, sauce, cheese, toppings):
        """
        Add a pizza to the order.
        
        This method creates a new Pizza object with the specified ingredients
        and adds it to the order, updating the total cost.
        
        Args:
            crust (str): Type of crust
            sauce (list): List of sauces
            cheese (str): Type of cheese
            toppings (list): List of toppings
            
        Example:
            >>> order = Order()
            >>> order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
            >>> len(order.pizzas)
            1
            >>> order.cost
            9
        """
        # Create a new pizza object
        pizza = Pizza(crust, sauce, cheese, toppings)
        
        # Add to the order
        self.pizzas.append(pizza)
        
        # Update the cost
        self.cost += pizza.cost()
    
    def order_paid(self):
        """
        Mark the order as paid.
        
        This method updates the payment status of the order to indicate
        that payment has been received.
        
        Example:
            >>> order = Order()
            >>> order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
            >>> order.paid
            False
            >>> order.order_paid()
            >>> order.paid
            True
        """
        self.paid = True