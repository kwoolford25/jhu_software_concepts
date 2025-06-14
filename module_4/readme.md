# Pizza Ordering System

A flexible framework for creating and managing pizza orders, built with Python and documented with Sphinx.

## Overview

This project implements a pizza ordering system that allows users to create orders with customized pizzas. The system calculates costs based on selected ingredients and tracks payment status. It was developed using Test-Driven Development (TDD) principles and includes comprehensive unit tests with pytest.

## Features

- Create customized pizza orders with various ingredients
- Calculate order costs automatically based on selected ingredients
- Track payment status for orders
- Support for multiple pizzas per order
- Extensible design for adding new ingredients

## Project Structure

```
module_4/
├── src/                  # Source code
│   ├── __init__.py
│   ├── order.py          # Order class implementation
│   └── pizza.py          # Pizza class implementation
├── tests/                # Test files
│   ├── __init__.py
│   ├── test_order.py     # Order class tests
│   ├── test_pizza.py     # Pizza class tests
│   └── test_integration.py  # Integration tests
├── docs/                 # Documentation source files
│   └── ...               # Sphinx documentation files
├── html_docs/            # Generated HTML documentation
├── demo.py               # Demo script to showcase functionality
├── pytest.ini            # Pytest configuration
└── requirements.txt      # Project dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kwoolford25/jhu_software_concepts.git
   cd jhu_software_concepts/module_4
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with specific markers:
```bash
pytest -m order  # Run only order-related tests
pytest -m pizza  # Run only pizza-related tests
```

## Usage

### Basic Example

```python
from src.order import Order

# Create a new order
order = Order()

# Add a pizza to the order
order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])

# Display the order
print(order)

# Mark the order as paid
order.order_paid()
```

### Demo Script

Run the included demo script to see the system in action:
```bash
python demo.py
```

## Available Options

### Crusts
- thin ($5)
- thick ($6)
- gluten_free ($8)

### Sauces
- marinara ($2)
- pesto ($3)
- liv_sauce ($5)

### Toppings
- pineapple ($1)
- pepperoni ($2)
- mushrooms ($3)

### Cheese
- mozzarella (included)

## Documentation

Full documentation is available at [Read the Docs](https://kwoolford-software-concepts.readthedocs.io/en/latest/).

### Viewing Documentation Locally

You can view the documentation locally in several ways:

1. **Open HTML directly**:
   ```bash
   # Navigate to the html_docs directory
   cd html_docs
   # Open index.html in your default browser
   start index.html  # On Windows
   open index.html   # On macOS
   xdg-open index.html  # On Linux
   ```

2. **Use Python's built-in HTTP server**:
   ```bash
   # Navigate to the html_docs directory
   cd html_docs
   # Start a simple HTTP server
   python -m http.server 8000
   # Then open http://localhost:8000 in your browser
   ```

3. **Build the documentation from source**:
   ```bash
   # Navigate to the docs directory
   cd docs
   # Build the HTML documentation
   sphinx-build -b html . _build/html
   # Open the built documentation
   start _build/html/index.html  # On Windows
   ```

## Development

This project was developed using Test-Driven Development (TDD) principles:
1. Write tests first
2. Run tests to verify they fail
3. Write code to make tests pass
4. Refactor code as needed

## License

This project is part of the JHU EP 605.256 – Modern Software Concepts in Python course.

## Author

Your Name