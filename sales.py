from datetime import datetime

from file_handler import (
    initialize_file,
    add_record,
    read_records
)

from product import ProductManager
from customer import CustomerManager


class Sale:

    def __init__(
        self,
        sale_id,
        customer_id,
        product_id,
        quantity,
        total
    ):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = int(quantity)
        self.total = float(total)
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_list(self):
        return [
            self.sale_id,
            self.customer_id,
            self.product_id,
            self.quantity,
            self.total,
            self.date
        ]


class SalesManager:

    FILE = "data/sales.csv"

    HEADERS = [
        "sale_id",
        "customer_id",
        "product_id",
        "quantity",
        "total",
        "date"
    ]

    def __init__(self):
        initialize_file(self.FILE, self.HEADERS)

    def generate_sale_id(self):
        records = read_records(self.FILE)

        if not records:
            return "S001"

        highest_id = 0

        for record in records:
            sale_id = record["sale_id"]

            if sale_id.startswith("S"):
                try:
                    number = int(sale_id[1:])

                    if number > highest_id:
                        highest_id = number

                except ValueError:
                    continue

        return f"S{highest_id + 1:03d}"

    def save_sale(self, sale):
        add_record(
            self.FILE,
            sale.to_list()
        )

        print("Sale recorded successfully.")

    def create_sale(self, customer_id, product_id, quantity):

        customer_manager = CustomerManager()
        product_manager = ProductManager()

        # Check customer
        customer = customer_manager.get_customer(customer_id)

        if customer is None:
            print("Customer not found.")
            return

        # Check product
        product = product_manager.get_product(product_id)

        if product is None:
            print("Product not found.")
            return

        # Validate quantity
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        # Check stock
        if quantity > product.quantity:
            print("Insufficient stock.")
            return

        # Calculate total
        total = product.price * quantity

        # Update inventory
        stock_updated = product_manager.reduce_stock(
            product_id,
            quantity
        )

        if not stock_updated:
            return

        # Generate sale ID
        sale_id = self.generate_sale_id()

        # Create sale object
        sale = Sale(
            sale_id,
            customer_id,
            product_id,
            quantity,
            total
        )

        # Save sale
        self.save_sale(sale)

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
        print(f"Date      : {sale.date}")

        print("=" * 35)

    def view_sales(self):
        records = read_records(self.FILE)

        if not records:
            print("No sales found.")
            return

        print("\n===== SALES HISTORY =====")

        for record in records:

            print(
                f"{record['sale_id']} | "
                f"Customer: {record['customer_id']} | "
                f"Product: {record['product_id']} | "
                f"Quantity: {record['quantity']} | "
                f"Total: ₹{float(record['total']):.2f} | "
                f"Date: {record['date']}"
            )