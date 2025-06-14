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
├── docs/                 # Documentation
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

You can also view the documentation locally:
```bash
cd docs
make html