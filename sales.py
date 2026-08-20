from datetime import datetime
from mysql.connector import Error

from database import create_connection
from product import Product
from customer import Customer


class Sale:

    def __init__(
        self,
        sale_id,
        customer_id,
        product_id,
        quantity,
        total,
        date=None
    ):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = int(quantity)
        self.total = float(total)

        if date:
            self.date = date
        else:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class SalesManager:

    def generate_sale_id(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
            SELECT sale_id
            FROM sales
            ORDER BY CAST(SUBSTRING(sale_id, 2) AS UNSIGNED) DESC
            LIMIT 1
        """

        cursor.execute(query)

        record = cursor.fetchone()

        cursor.close()
        connection.close()

        if record is None:
            return "S001"

        highest_id = int(record[0][1:])

        return f"S{highest_id + 1:03d}"


    def create_sale(self, customer_id, product_id, quantity):

        connection = create_connection()

        if connection is None:
            print("Unable to connect to database.")
            return

        cursor = connection.cursor()

        try:

            # Start transaction
            connection.start_transaction()

            # Check customer
            cursor.execute(
                """
                SELECT customer_id, name, phone
                FROM customers
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            customer_record = cursor.fetchone()

            if customer_record is None:
                print("Customer not found.")
                connection.rollback()
                return

            customer = Customer(
                customer_record[0],
                customer_record[1],
                customer_record[2]
            )

            # Check product
            cursor.execute(
                """
                SELECT product_id, name, category, price, quantity
                FROM products
                WHERE product_id = %s
                """,
                (product_id,)
            )

            product_record = cursor.fetchone()

            if product_record is None:
                print("Product not found.")
                connection.rollback()
                return

            product = Product(
                product_record[0],
                product_record[1],
                product_record[2],
                product_record[3],
                product_record[4]
            )

            # Validate quantity
            if quantity <= 0:
                print("Quantity must be greater than zero.")
                connection.rollback()
                return

            # Check stock
            if quantity > product.quantity:
                print("Insufficient stock.")
                connection.rollback()
                return

            # Calculate total
            total = product.price * quantity

            # Generate sale ID
            cursor.execute(
                """
                SELECT sale_id
                FROM sales
                ORDER BY CAST(SUBSTRING(sale_id, 2) AS UNSIGNED) DESC
                LIMIT 1
                """
            )

            last_sale = cursor.fetchone()

            if last_sale is None:
                sale_id = "S001"
            else:
                highest_id = int(last_sale[0][1:])
                sale_id = f"S{highest_id + 1:03d}"

            sale_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            cursor.execute(
                """
                UPDATE products
                SET quantity = quantity - %s
                WHERE product_id = %s
                AND quantity >= %s
                """,
                (quantity, product_id, quantity)
            )

            if cursor.rowcount == 0:
                print("Insufficient stock.")
                connection.rollback()
                return

            # Insert sale
            cursor.execute(
                """
                INSERT INTO sales
                (sale_id, customer_id, product_id, quantity, total, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    sale_id,
                    customer_id,
                    product_id,
                    quantity,
                    total,
                    sale_date
                )
            )

            # Everything succeeded
            connection.commit()

            print("Sale recorded successfully.")

            # Generate bill
            print("\n" + "=" * 35)
            print("              BILL")
            print("=" * 35)

            print(f"Sale ID   : {sale_id}")
            print(f"Customer  : {customer.name}")
            print(f"Product   : {product.name}")
            print(f"Quantity  : {quantity}")
            print(f"Price     : ₹{product.price:.2f}")
            print(f"Total     : ₹{total:.2f}")
            print(f"Date      : {sale_date}")

            print("=" * 35)

        except Error as e:

            connection.rollback()

            print("Sale failed.")
            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()

    def view_sales(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
                SELECT
                    sale_id,
                    customer_id,
                    product_id,
                    quantity,
                    total,
                    date
                FROM sales
                ORDER BY sale_id
            """

            cursor.execute(query)

            records = cursor.fetchall()

            if not records:
                print("No sales found.")
                return

            print("\n===== SALES HISTORY =====")

            for record in records:

                print(
                    f"{record[0]} | "
                    f"Customer: {record[1]} | "
                    f"Product: {record[2]} | "
                    f"Quantity: {record[3]} | "
                    f"Total: ₹{float(record[4]):.2f} | "
                    f"Date: {record[5]}"
                )

        except Error as e:

            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()