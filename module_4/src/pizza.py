class Pizza:
    """Pizza class for creating and managing pizza objects."""
    
    # Define price constants
    CRUST_PRICES = {
        "thin": 5,
        "thick": 6,
        "gluten_free": 8
    }
    
    SAUCE_PRICES = {
        "marinara": 2,
        "pesto": 3,
        "liv_sauce": 5
    }
    
    TOPPING_PRICES = {
        "pineapple": 1,
        "pepperoni": 2,
        "mushrooms": 3
    }
    
    def __init__(self, crust, sauce, cheese, toppings):
        """
        Initialize a pizza with specified ingredients.
        
        Args:
            crust (str): Type of crust (thin, thick, or gluten_free)
            sauce (list): List of sauces (marinara, pesto, liv_sauce)
            cheese (str): Type of cheese (only mozzarella supported)
            toppings (list): List of toppings (pineapple, pepperoni, mushrooms)
        """
        # Validate inputs
        if crust not in self.CRUST_PRICES:
            raise ValueError(f"Invalid crust type: {crust}")
            
        for s in sauce:
            if s not in self.SAUCE_PRICES:
                raise ValueError(f"Invalid sauce type: {s}")
                
        if cheese != "mozzarella":
            raise ValueError("Only mozzarella cheese is supported")
            
        for t in toppings:
            if t not in self.TOPPING_PRICES:
                raise ValueError(f"Invalid topping: {t}")
        
        # Ensure at least one sauce and one topping
        if not sauce:
            raise ValueError("Pizza must include at least one sauce")
            
        if not toppings:
            raise ValueError("Pizza must include at least one topping")
        
        # Set pizza variables
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings
    
    def __str__(self):
        """
        Return a string representation of the pizza.
        
        Returns:
            str: Description of the pizza and its cost
        """
        sauce_str = ", ".join(self.sauce)
        toppings_str = ", ".join(self.toppings)
        
        return f"{self.crust.title()} crust pizza with {sauce_str} sauce, {self.cheese} cheese, " \
               f"and {toppings_str}. Cost: ${self.cost()}"
    
    def cost(self):
        """
        Calculate the cost of the pizza based on its ingredients.
        
        Returns:
            int: Total cost of the pizza
        """
        total_cost = 0
        
        # Add crust cost
        total_cost += self.CRUST_PRICES[self.crust]
        
        # Add sauce costs
        for sauce in self.sauce:
            total_cost += self.SAUCE_PRICES[sauce]
        
        # Add topping costs
        for topping in self.toppings:
            total_cost += self.TOPPING_PRICES[topping]
        
        return total_cost