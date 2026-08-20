from multiprocessing import connection

from database import create_connection
from mysql.connector import Error


class Product:

    def __init__(self, product_id, name, category, price, quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity = int(quantity)

    def display(self):
        print(
            f"{self.product_id} | "
            f"{self.name} | "
            f"{self.category} | "
            f"₹{self.price:.2f} | "
            f"Stock: {self.quantity}"
        )


class ProductManager:

    def add_product(self, product):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        # Check if product already exists
        query = """
            SELECT product_id
            FROM products
            WHERE product_id = %s
        """

        cursor.execute(query, (product.product_id,))

        if cursor.fetchone():
            print("Product ID already exists.")

            cursor.close()
            connection.close()
            return

        # Insert product
        query = """
            INSERT INTO products
            (product_id, name, category, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            product.product_id,
            product.name,
            product.category,
            product.price,
            product.quantity
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        print("Product added successfully.")

    def view_products(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            SELECT product_id, name, category, price, quantity
            FROM products
            ORDER BY product_id
        """

        cursor.execute(query)

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        if not records:
            print("No products found.")
            return

        print("\n===== PRODUCT LIST =====")

        for record in records:

            product = Product(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4]
            )

            product.display()

    def search_product(self, product_id):

        product = self.get_product(product_id)

        if product:
            product.display()
        else:
            print("Product not found.")

    def update_product(self, product_id, new_price, new_quantity):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            UPDATE products
            SET price = %s,
                quantity = %s
            WHERE product_id = %s
        """

        values = (
            new_price,
            new_quantity,
            product_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:
            print("Product not found.")
        else:
            connection.commit()
            print("Product updated successfully.")

        cursor.close()
        connection.close()

    def delete_product(self, product_id):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            DELETE FROM products
            WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))

        if cursor.rowcount == 0:
            print("Product not found.")
        else:
            connection.commit()
            print("Product deleted successfully.")

        cursor.close()
        connection.close()

    def reduce_stock(self, product_id, quantity):

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return False

        connection = create_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        # Get current stock
        query = """
            SELECT quantity
            FROM products
            WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))

        record = cursor.fetchone()

        if record is None:
            print("Product not found.")

            cursor.close()
            connection.close()
            return False

        current_stock = int(record[0])

        if quantity > current_stock:
            print("Insufficient stock.")

            cursor.close()
            connection.close()
            return False

        # Update stock
        new_stock = current_stock - quantity

        query = """
            UPDATE products
            SET quantity = %s
            WHERE product_id = %s
        """

        cursor.execute(
            query,
            (new_stock, product_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    def get_product(self, product_id):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            SELECT product_id, name, category, price, quantity
            FROM products
            WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))

        record = cursor.fetchone()

        cursor.close()
        connection.close()

        if record:

            return Product(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4]
            )

        return None