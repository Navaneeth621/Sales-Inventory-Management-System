from database import create_connection
from product import Product
from mysql.connector import Error


class ReportManager:

    def sales_summary(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
                SELECT
                    COUNT(*) AS total_transactions,
                    COALESCE(SUM(total), 0) AS total_revenue,
                    COALESCE(AVG(total), 0) AS average_sale
                FROM sales
            """

            cursor.execute(query)

            record = cursor.fetchone()

            total_transactions = record[0]
            total_revenue = float(record[1])
            average_sale = float(record[2])

            if total_transactions == 0:
                print("No sales data available.")
                return

            print("\n===== SALES REPORT =====")
            print(f"Total Transactions : {total_transactions}")
            print(f"Total Revenue      : ₹{total_revenue:.2f}")
            print(f"Average Sale       : ₹{average_sale:.2f}")

        except Error as e:

            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()

    def low_stock_report(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
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

            cursor.execute(query)

            records = cursor.fetchall()

            print("\n===== LOW STOCK PRODUCTS =====")

            if not records:
                print("No low-stock products.")
                return

            for record in records:

                product = Product(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4]
                )

                product.display()

        except Error as e:

            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()