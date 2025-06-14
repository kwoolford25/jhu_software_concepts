from src.pizza import Pizza

class Order:
    """Order class for managing customer pizza orders."""
    
    def __init__(self):
        """Initialize a customer order with empty pizza list and zero cost."""
        self.pizzas = []
        self.cost = 0
        self.paid = False
    
    def __str__(self):
        """
        Return a string representation of the complete order.
        
        Returns:
            str: Description of all pizzas in the order and total cost
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
        
        Args:
            crust (str): Type of crust
            sauce (list): List of sauces
            cheese (str): Type of cheese
            toppings (list): List of toppings
        """
        # Create a new pizza object
        pizza = Pizza(crust, sauce, cheese, toppings)
        
        # Add to the order
        self.pizzas.append(pizza)
        
        # Update the cost
        self.cost += pizza.cost()
    
    def order_paid(self):
        """Mark the order as paid."""
        self.paid = True