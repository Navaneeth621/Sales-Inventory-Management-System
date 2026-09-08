import sys
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mysql.connector import Error


# ============================================================
# PROJECT ROOT
# ============================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ============================================================
# DATABASE
# ============================================================

from database import create_connection


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Smart Sales & Inventory Management API",
    description="Backend API for Sales and Inventory Management System",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PYDANTIC MODELS
# ============================================================

class ProductCreate(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    quantity: int


class ProductUpdate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class CustomerCreate(BaseModel):
    customer_id: str
    name: str
    phone: str


class CustomerUpdate(BaseModel):
    name: str
    phone: str


class SaleCreate(BaseModel):
    customer_id: str
    product_id: str
    quantity: int


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Smart Sales & Inventory Management API is running"
    }


# ============================================================
# PRODUCT APIs
# ============================================================

@app.get("/products")
def get_products():

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                product_id,
                name,
                category,
                price,
                quantity
            FROM products
            ORDER BY product_id
            """
        )

        products = cursor.fetchall()

        for product in products:
            product["price"] = float(product["price"])
            product["quantity"] = int(product["quantity"])

        return products

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.get("/products/{product_id}")
def get_product(product_id: str):

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                product_id,
                name,
                category,
                price,
                quantity
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if product is None:

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product["price"] = float(product["price"])
        product["quantity"] = int(product["quantity"])

        return product

    except HTTPException:

        raise

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.post("/products")
def create_product(product: ProductCreate):

    if product.price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Price must be greater than zero"
        )

    if product.quantity < 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    if not product.product_id.strip():

        raise HTTPException(
            status_code=400,
            detail="Product ID cannot be empty"
        )

    if not product.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Product name cannot be empty"
        )

    if not product.category.strip():

        raise HTTPException(
            status_code=400,
            detail="Category cannot be empty"
        )

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT product_id
            FROM products
            WHERE product_id = %s
            """,
            (product.product_id,)
        )

        if cursor.fetchone():

            raise HTTPException(
                status_code=409,
                detail="Product ID already exists"
            )

        cursor.execute(
            """
            INSERT INTO products
            (
                product_id,
                name,
                category,
                price,
                quantity
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                product.product_id,
                product.name,
                product.category,
                product.price,
                product.quantity
            )
        )

        connection.commit()

        return {
            "message": "Product added successfully",
            "product": {
                "product_id": product.product_id,
                "name": product.name,
                "category": product.category,
                "price": product.price,
                "quantity": product.quantity
            }
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.put("/products/{product_id}")
def update_product(
    product_id: str,
    product: ProductUpdate
):

    if product.price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Price must be greater than zero"
        )

    if product.quantity < 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity cannot be negative"
        )

    if not product.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Product name cannot be empty"
        )

    if not product.category.strip():

        raise HTTPException(
            status_code=400,
            detail="Category cannot be empty"
        )

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT product_id
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        if cursor.fetchone() is None:

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        cursor.execute(
            """
            UPDATE products
            SET
                name = %s,
                category = %s,
                price = %s,
                quantity = %s
            WHERE product_id = %s
            """,
            (
                product.name,
                product.category,
                product.price,
                product.quantity,
                product_id
            )
        )

        connection.commit()

        return {
            "message": "Product updated successfully",
            "product_id": product_id
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.delete("/products/{product_id}")
def delete_product(product_id: str):

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT product_id
            FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        if cursor.fetchone() is None:

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        cursor.execute(
            """
            DELETE FROM products
            WHERE product_id = %s
            """,
            (product_id,)
        )

        connection.commit()

        return {
            "message": "Product deleted successfully",
            "product_id": product_id
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# CUSTOMER APIs
# ============================================================

@app.get("/customers")
def get_customers():

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                phone
            FROM customers
            ORDER BY customer_id
            """
        )

        return cursor.fetchall()

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                phone
            FROM customers
            WHERE customer_id = %s
            """,
            (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:

            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return customer

    except HTTPException:

        raise

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.post("/customers")
def create_customer(customer: CustomerCreate):

    if not customer.customer_id.strip():

        raise HTTPException(
            status_code=400,
            detail="Customer ID cannot be empty"
        )

    if not customer.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Customer name cannot be empty"
        )

    if not customer.phone.isdigit() or len(customer.phone) != 10:

        raise HTTPException(
            status_code=400,
            detail="Phone number must be exactly 10 digits"
        )

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE customer_id = %s
            """,
            (customer.customer_id,)
        )

        if cursor.fetchone():

            raise HTTPException(
                status_code=409,
                detail="Customer ID already exists"
            )

        cursor.execute(
            """
            INSERT INTO customers
            (
                customer_id,
                name,
                phone
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                customer.customer_id,
                customer.name,
                customer.phone
            )
        )

        connection.commit()

        return {
            "message": "Customer added successfully",
            "customer": {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "phone": customer.phone
            }
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.put("/customers/{customer_id}")
def update_customer(
    customer_id: str,
    customer: CustomerUpdate
):

    if not customer.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Customer name cannot be empty"
        )

    if not customer.phone.isdigit() or len(customer.phone) != 10:

        raise HTTPException(
            status_code=400,
            detail="Phone number must be exactly 10 digits"
        )

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE customer_id = %s
            """,
            (customer_id,)
        )

        if cursor.fetchone() is None:

            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        cursor.execute(
            """
            UPDATE customers
            SET
                name = %s,
                phone = %s
            WHERE customer_id = %s
            """,
            (
                customer.name,
                customer.phone,
                customer_id
            )
        )

        connection.commit()

        return {
            "message": "Customer updated successfully",
            "customer_id": customer_id
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT customer_id
            FROM customers
            WHERE customer_id = %s
            """,
            (customer_id,)
        )

        if cursor.fetchone() is None:

            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        cursor.execute(
            """
            DELETE FROM customers
            WHERE customer_id = %s
            """,
            (customer_id,)
        )

        connection.commit()

        return {
            "message": "Customer deleted successfully",
            "customer_id": customer_id
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# SALES APIs
# ============================================================

@app.get("/sales")
def get_sales():

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                sale_id,
                customer_id,
                product_id,
                quantity,
                total,
                date
            FROM sales
            ORDER BY
                CAST(SUBSTRING(sale_id, 2) AS UNSIGNED)
            """
        )

        sales = cursor.fetchall()

        for sale in sales:
            sale["total"] = float(sale["total"])
            sale["quantity"] = int(sale["quantity"])

        return sales

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.get("/sales/{sale_id}")
def get_sale(sale_id: str):

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                sale_id,
                customer_id,
                product_id,
                quantity,
                total,
                date
            FROM sales
            WHERE sale_id = %s
            """,
            (sale_id,)
        )

        sale = cursor.fetchone()

        if sale is None:

            raise HTTPException(
                status_code=404,
                detail="Sale not found"
            )

        sale["total"] = float(sale["total"])
        sale["quantity"] = int(sale["quantity"])

        return sale

    except HTTPException:

        raise

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.post("/sales")
def create_sale(sale: SaleCreate):

    if sale.quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        connection.start_transaction()

        # ----------------------------------------------------
        # Check customer
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                phone
            FROM customers
            WHERE customer_id = %s
            """,
            (sale.customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:

            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # ----------------------------------------------------
        # Check product
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                product_id,
                name,
                category,
                price,
                quantity
            FROM products
            WHERE product_id = %s
            FOR UPDATE
            """,
            (sale.product_id,)
        )

        product = cursor.fetchone()

        if product is None:

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        # ----------------------------------------------------
        # Check stock
        # ----------------------------------------------------

        if sale.quantity > product["quantity"]:

            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        # ----------------------------------------------------
        # Calculate total
        # ----------------------------------------------------

        total = float(product["price"]) * sale.quantity

        # ----------------------------------------------------
        # Generate sale ID
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT sale_id
            FROM sales
            ORDER BY
                CAST(SUBSTRING(sale_id, 2) AS UNSIGNED) DESC
            LIMIT 1
            """
        )

        last_sale = cursor.fetchone()

        if last_sale is None:

            sale_id = "S001"

        else:

            highest_id = int(
                last_sale["sale_id"][1:]
            )

            sale_id = f"S{highest_id + 1:03d}"

        sale_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # ----------------------------------------------------
        # Reduce stock
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE products
            SET quantity = quantity - %s
            WHERE product_id = %s
            AND quantity >= %s
            """,
            (
                sale.quantity,
                sale.product_id,
                sale.quantity
            )
        )

        if cursor.rowcount == 0:

            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        # ----------------------------------------------------
        # Insert sale
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO sales
            (
                sale_id,
                customer_id,
                product_id,
                quantity,
                total,
                date
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                sale_id,
                sale.customer_id,
                sale.product_id,
                sale.quantity,
                total,
                sale_date
            )
        )

        connection.commit()

        return {
            "message": "Sale recorded successfully",
            "sale": {
                "sale_id": sale_id,
                "customer_id": sale.customer_id,
                "customer_name": customer["name"],
                "product_id": sale.product_id,
                "product_name": product["name"],
                "quantity": sale.quantity,
                "price": float(product["price"]),
                "total": total,
                "date": sale_date
            }
        }

    except HTTPException:

        connection.rollback()
        raise

    except Error as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Sale failed: {e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# REPORT APIs
# ============================================================

@app.get("/reports/sales")
def sales_report():

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_transactions,
                COALESCE(SUM(total), 0) AS total_revenue,
                COALESCE(AVG(total), 0) AS average_sale
            FROM sales
            """
        )

        record = cursor.fetchone()

        return {
            "total_transactions": int(
                record["total_transactions"]
            ),
            "total_revenue": float(
                record["total_revenue"]
            ),
            "average_sale": float(
                record["average_sale"]
            )
        }

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()


@app.get("/reports/low-stock")
def low_stock_report():

    connection = create_connection()

    if connection is None:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                product_id,
                name,
                category,
                price,
                quantity
            FROM products
            WHERE quantity <= 5
            ORDER BY quantity
            """
        )

        products = cursor.fetchall()

        for product in products:

            product["price"] = float(
                product["price"]
            )

            product["quantity"] = int(
                product["quantity"]
            )

        # Return the array directly because
        # App.jsx expects lowStockProducts.map(...)
        return products

    except Error as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )

    finally:

        cursor.close()
        connection.close()