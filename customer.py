from database import create_connection
from mysql.connector import Error

class Customer:

    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone

    def display(self):
        print(
            f"{self.customer_id} | "
            f"{self.name} | "
            f"{self.phone}"
        )


class CustomerManager:

    def add_customer(self, customer):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
                SELECT customer_id
                FROM customers
                WHERE customer_id = %s
            """

            cursor.execute(query, (customer.customer_id,))

            if cursor.fetchone():
                print("Customer ID already exists.")
                return

            query = """
                INSERT INTO customers
                (customer_id, name, phone)
                VALUES (%s, %s, %s)
            """

            values = (
                customer.customer_id,
                customer.name,
                customer.phone
            )

            cursor.execute(query, values)

            connection.commit()

            print("Customer added successfully.")

        except Error as e:

            connection.rollback()
            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()

    def view_customers(self):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
                SELECT customer_id, name, phone
                FROM customers
                ORDER BY customer_id
            """

            cursor.execute(query)

            records = cursor.fetchall()

            if not records:
                print("No customers found.")
                return

            print("\n===== CUSTOMER LIST =====")

            for record in records:

                customer = Customer(
                    record[0],
                    record[1],
                    record[2]
                )

                customer.display()

        except Error as e:

            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()

    def search_customer(self, customer_id):

        customer = self.get_customer(customer_id)

        if customer:
            customer.display()
        else:
            print("Customer not found.")

    def update_customer(self, customer_id, new_name, new_phone):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
                UPDATE customers
                SET name = %s,
                    phone = %s
                WHERE customer_id = %s
            """

            values = (
                new_name,
                new_phone,
                customer_id
            )

            cursor.execute(query, values)

            if cursor.rowcount == 0:
                print("Customer not found.")
            else:
                connection.commit()
                print("Customer updated successfully.")

        except Error as e:

            connection.rollback()
            print("Database error:", e)

        finally:

            cursor.close()
            connection.close()

    def delete_customer(self, customer_id):

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        try:

            query = """
                DELETE FROM customers
                WHERE customer_id = %s
            """

            cursor.execute(query, (customer_id,))

            if cursor.rowcount == 0:
                print("Customer not found.")
            else:
                connection.commit()
                print("Customer deleted successfully.")

        except Error as e:

            connection.rollback()

            if e.errno == 1451:
                print("Cannot delete customer.")
                print("Customer has existing sales records.")
            else:
                print("Database error:", e)

        finally:

            cursor.close()
            connection.close()

    def get_customer(self, customer_id):

        connection = create_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:

            query = """
                SELECT customer_id, name, phone
                FROM customers
                WHERE customer_id = %s
            """

            cursor.execute(query, (customer_id,))

            record = cursor.fetchone()

            if record:

                return Customer(
                    record[0],
                    record[1],
                    record[2]
                )

            return None

        except Error as e:

            print("Database error:", e)
            return None

        finally:

            cursor.close()
            connection.close()