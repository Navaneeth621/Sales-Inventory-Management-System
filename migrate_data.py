import csv
from database import create_connection


def migrate_products():
    connection = create_connection()
    
    if connection is None:
        return
    
    cursor = connection.cursor()

    with open("data/products.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            query = """
                INSERT INTO products
                (product_id, name, category, price, quantity)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                row["product_id"],
                row["name"],
                row["category"],
                float(row["price"]),
                int(row["quantity"])
            )

            cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Products migrated successfully.")


def migrate_customers():
    connection = create_connection()
    
    if connection is None:
        return
    
    cursor = connection.cursor()

    with open("data/customers.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            query = """
                INSERT INTO customers
                (customer_id, name, phone)
                VALUES (%s, %s, %s)
            """

            values = (
                row["customer_id"],
                row["name"],
                row["phone"]
            )

            cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Customers migrated successfully.")


def migrate_sales():
    connection = create_connection()
    
    if connection is None:
        return
    
    cursor = connection.cursor()

    with open("data/sales.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            query = """
                INSERT INTO sales
                (sale_id, customer_id, product_id, quantity, total, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                row["sale_id"],
                row["customer_id"],
                row["product_id"],
                int(row["quantity"]),
                float(row["total"]),
                row["date"]
            )

            cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Sales migrated successfully.")


if __name__ == "__main__":
    migrate_sales()