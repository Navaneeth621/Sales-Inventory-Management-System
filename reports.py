from file_handler import read_records
from product import Product


class ReportManager:

    SALES_FILE = "data/sales.csv"
    PRODUCTS_FILE = "data/products.csv"

    def sales_summary(self):
        records = read_records(self.SALES_FILE)

        if not records:
            print("No sales data available.")
            return

        total_transactions = len(records)
        total_revenue = 0

        for record in records:
            total_revenue += float(record["total"])

        average_sale = total_revenue / total_transactions

        print("\n===== SALES REPORT =====")
        print(f"Total Transactions : {total_transactions}")
        print(f"Total Revenue      : ₹{total_revenue:.2f}")
        print(f"Average Sale       : ₹{average_sale:.2f}")

    def low_stock_report(self):
        products = read_records(self.PRODUCTS_FILE)

        print("\n===== LOW STOCK PRODUCTS =====")

        found = False

        for record in products:

            quantity = int(record["quantity"])

            if quantity <= 5:

                product = Product(
                    record["product_id"],
                    record["name"],
                    record["category"],
                    record["price"],
                    record["quantity"]
                )

                product.display()

                found = True

        if not found:
            print("No low-stock products.")