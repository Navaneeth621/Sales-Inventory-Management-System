from file_handler import (
    initialize_file,
    add_record,
    read_records
)


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

    def to_list(self):
        return [
            self.customer_id,
            self.name,
            self.phone
        ]


class CustomerManager:

    FILE = "data/customers.csv"

    HEADERS = [
        "customer_id",
        "name",
        "phone"
    ]

    def __init__(self):
        initialize_file(self.FILE, self.HEADERS)

    def add_customer(self, customer):
        records = read_records(self.FILE)

        for record in records:
            if record["customer_id"] == customer.customer_id:
                print("Customer ID already exists.")
                return

        add_record(
            self.FILE,
            customer.to_list()
        )

        print("Customer added successfully.")

    def view_customers(self):
        records = read_records(self.FILE)

        if not records:
            print("No customers found.")
            return

        print("\n===== CUSTOMER LIST =====")

        for record in records:

            customer = Customer(
                record["customer_id"],
                record["name"],
                record["phone"]
            )

            customer.display()

    def search_customer(self, customer_id):
        customer = self.get_customer(customer_id)

        if customer:
            customer.display()
        else:
            print("Customer not found.")

    def get_customer(self, customer_id):
        records = read_records(self.FILE)

        for record in records:

            if record["customer_id"] == customer_id:

                return Customer(
                    record["customer_id"],
                    record["name"],
                    record["phone"]
                )

        return None