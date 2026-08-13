# Smart Sales & Inventory Management System

A console-based Sales & Inventory Management System developed using Python and Object-Oriented Programming (OOP). The project is designed to help small businesses manage products, customers, inventory, sales transactions, and basic business reports efficiently.

## Project Overview

Managing products, customers, stock, and sales manually can become difficult and error-prone for small businesses. This project provides a simple command-line solution to organize these activities in one system.

The application uses Python for the core functionality and CSV files for persistent data storage. It demonstrates Python fundamentals, Object-Oriented Programming, file handling, exception handling, and modular programming.

## Key Features

### Product Management
- Add new products
- View all products
- Search products by ID
- Update product price and quantity
- Delete products
- Prevent duplicate product IDs
- Validate price and quantity
- Automatically update stock after a sale

### Customer Management
- Add new customers
- View customers
- Search customers by ID
- Prevent duplicate customer IDs
- Validate customer phone numbers

### Sales Management
- Create sales transactions
- Validate customer and product details
- Check product availability
- Validate sale quantity
- Prevent sales when stock is insufficient
- Automatically reduce inventory after a successful sale
- Generate unique sale IDs
- Generate a detailed bill
- Maintain sales history

### Reports
- View sales history
- Calculate total transactions
- Calculate total revenue
- Calculate average sale value
- Identify low-stock products

## Technologies Used

- Python 3.11
- Object-Oriented Programming (OOP)
- CSV File Handling
- Exception Handling
- `datetime` module
- Python Lists and Dictionaries
- Functions and Modules

## Python Concepts Demonstrated

This project applies several Python concepts, including:

- Variables and data types
- Strings
- Lists
- Dictionaries
- Conditional statements
- Loops
- Functions
- Modules
- Classes and objects
- Constructors
- Instance variables and methods
- Encapsulation
- List comprehension
- File handling
- CSV processing
- Exception handling
- Date and time handling

## OOP Design

The project uses separate classes based on real-world entities and responsibilities.

```text
Product
   |
ProductManager
   |
products.csv
