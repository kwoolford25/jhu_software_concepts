from src.order import Order

def main():
    print("Pizza Ordering System Demo\n")
    
    # Create Order 1
    print("Creating Order 1...")
    order1 = Order()
    
    # Add pizzas to Order 1
    print("Adding pizzas to Order 1:")
    order1.input_pizza("thin", ["pesto"], "mozzarella", ["mushrooms"])
    order1.input_pizza("thick", ["marinara"], "mozzarella", ["mushrooms"])
    
    # Display Order 1
    print("\nOrder 1 Details:")
    print(order1)
    
    # Mark Order 1 as paid
    print("\nMarking Order 1 as paid...")
    order1.order_paid()
    print("After payment:")
    print(order1)
    
    # Create Order 2
    print("\n" + "-"*50 + "\n")
    print("Creating Order 2...")
    order2 = Order()
    
    # Add pizzas to Order 2
    print("Adding pizzas to Order 2:")
    order2.input_pizza("gluten_free", ["marinara"], "mozzarella", ["pineapple"])
    order2.input_pizza("thin", ["liv_sauce", "pesto"], "mozzarella", ["mushrooms", "pepperoni"])
    
    # Display Order 2
    print("\nOrder 2 Details:")
    print(order2)
    
    # Calculate and display total costs
    print("\n" + "-"*50)
    print(f"Order 1 Total Cost: ${order1.cost}")
    print(f"Order 2 Total Cost: ${order2.cost}")

if __name__ == "__main__":
    main()