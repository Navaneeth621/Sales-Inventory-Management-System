from file_handler import (
    initialize_file,
    add_record,
    read_records,
    write_records
)


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

    def to_list(self):
        return [
            self.product_id,
            self.name,
            self.category,
            self.price,
            self.quantity
        ]


class ProductManager:

    FILE = "data/products.csv"

    HEADERS = [
        "product_id",
        "name",
        "category",
        "price",
        "quantity"
    ]

    def __init__(self):
        initialize_file(self.FILE, self.HEADERS)

    def add_product(self, product):
        records = read_records(self.FILE)

        for record in records:
            if record["product_id"] == product.product_id:
                print("Product ID already exists.")
                return

        add_record(self.FILE, product.to_list())

        print("Product added successfully.")

    def view_products(self):
        records = read_records(self.FILE)

        if not records:
            print("No products found.")
            return

        print("\n===== PRODUCT LIST =====")

        for record in records:
            product = Product(
                record["product_id"],
                record["name"],
                record["category"],
                record["price"],
                record["quantity"]
            )

            product.display()

    def search_product(self, product_id):
        product = self.get_product(product_id)

        if product:
            product.display()
        else:
            print("Product not found.")

    def update_product(self, product_id, new_price, new_quantity):
        records = read_records(self.FILE)

        for record in records:
            if record["product_id"] == product_id:

                record["price"] = str(new_price)
                record["quantity"] = str(new_quantity)

                write_records(
                    self.FILE,
                    records,
                    self.HEADERS
                )

                print("Product updated successfully.")
                return

        print("Product not found.")

    def delete_product(self, product_id):
        records = read_records(self.FILE)

        new_records = [
            record
            for record in records
            if record["product_id"] != product_id
        ]

        if len(new_records) == len(records):
            print("Product not found.")
            return

        write_records(
            self.FILE,
            new_records,
            self.HEADERS
        )

        print("Product deleted successfully.")

    def reduce_stock(self, product_id, quantity):

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return False

        records = read_records(self.FILE)

        for record in records:

            if record["product_id"] == product_id:

                current_stock = int(record["quantity"])

                if quantity > current_stock:
                    print("Insufficient stock.")
                    return False

                record["quantity"] = str(
                    current_stock - quantity
                )

                write_records(
                    self.FILE,
                    records,
                    self.HEADERS
                )

                return True

        print("Product not found.")
        return False

    def get_product(self, product_id):
        records = read_records(self.FILE)

        for record in records:

            if record["product_id"] == product_id:

                return Product(
                    record["product_id"],
                    record["name"],
                    record["category"],
                    record["price"],
                    record["quantity"]
                )

        return None