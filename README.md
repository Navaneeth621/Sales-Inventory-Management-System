# Smart Sales & Inventory Management System

A full-stack Sales & Inventory Management System designed to help small businesses manage products, customers, inventory, sales transactions, and business reports efficiently.

The project was developed incrementally using Python and Object-Oriented Programming, MySQL, FastAPI, and React.

## Project Overview

Managing products, customers, stock, and sales manually can become difficult and error-prone for small businesses.

This project provides a centralized application where users can:

- Manage products and inventory
- Manage customer information
- Create and track sales transactions
- Automatically update product stock after sales
- View sales history
- Analyze revenue and sales performance
- Monitor low-stock products

The project started as a console-based Python application and was later upgraded to use MySQL for persistent storage, FastAPI for REST APIs, and React for the frontend.

---

## Key Features

### Dashboard

- View total products
- View total customers
- View total sales transactions
- View total revenue
- View recent sales
- Monitor low-stock products
- Quick access to common operations

### Product Management

- Add new products
- View all products
- Search products
- Search by product ID, name, or category
- Update product information
- Update price and stock quantity
- Delete products
- Prevent duplicate product IDs
- Validate price and quantity
- Automatically reduce stock after successful sales

### Customer Management

- Add new customers
- View all customers
- Search customers
- Search by customer ID, name, or phone number
- Update customer information
- Delete customers
- Prevent duplicate customer IDs
- Validate customer phone numbers

### Sales Management

- Create sales transactions
- Select customers and products
- Validate customer and product details
- Check product availability
- Validate sale quantity
- Prevent sales when stock is insufficient
- Automatically reduce inventory after successful sales
- Generate unique sale IDs
- Calculate total sale amount
- Generate a detailed bill
- Maintain sales history

### Reports

- View sales summary
- Calculate total transactions
- Calculate total revenue
- Calculate average sale value
- View revenue trends
- View inventory status
- Identify low-stock products
- Display report data using charts

---

## System Architecture

```text
                  React Frontend
                       |
                       | HTTP Requests
                       v
                 FastAPI Backend
                       |
                       | SQL Queries
                       v
                  MySQL Database
