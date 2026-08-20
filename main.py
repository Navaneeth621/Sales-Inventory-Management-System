from product import Product, ProductManager
from customer import Customer, CustomerManager
from sales import SalesManager
from reports import ReportManager


# Create manager objects
product_manager = ProductManager()
customer_manager = CustomerManager()
sales_manager = SalesManager()
report_manager = ReportManager()


def product_menu():

    while True:

        print("\n===== PRODUCT MANAGEMENT =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        # Add Product
        if choice == "1":

            product_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            category = input("Enter Category: ")

            if not product_id or not name or not category:
                print("Product ID, name, and category cannot be empty.")
                continue

            try:
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))

            except ValueError:
                print("Please enter valid numeric values.")
                continue

            if price <= 0:
                print("Price must be greater than zero.")
                continue

            if quantity < 0:
                print("Quantity cannot be negative.")
                continue

            product = Product(
                product_id,
                name,
                category,
                price,
                quantity
            )

            product_manager.add_product(product)

        # View Products
        elif choice == "2":

            product_manager.view_products()

        # Search Product
        elif choice == "3":

            product_id = input("Enter Product ID: ")
            product_manager.search_product(product_id)

        # Update Product
        elif choice == "4":

            product_id = input("Enter Product ID: ")

            try:
                price = float(input("Enter New Price: "))
                quantity = int(input("Enter New Quantity: "))

            except ValueError:
                print("Please enter valid numeric values.")
                continue

            if price <= 0:
                print("Price must be greater than zero.")
                continue

            if quantity < 0:
                print("Quantity cannot be negative.")
                continue

            product_manager.update_product(
                product_id,
                price,
                quantity
            )

        # Delete Product
        elif choice == "5":

            product_id = input("Enter Product ID: ")
            product_manager.delete_product(product_id)

        # Back to Main Menu
        elif choice == "6":

            break

        else:

            print("Invalid choice. Please try again.")


def customer_menu():

    while True:

        print("\n===== CUSTOMER MANAGEMENT =====")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        # Add Customer
        if choice == "1":

            customer_id = input("Enter Customer ID: ")
            name = input("Enter Customer Name: ")
            phone = input("Enter Phone Number: ")

            if not customer_id or not name:
                print("Customer ID and name cannot be empty.")
                continue

            if not phone.isdigit() or len(phone) != 10:
                print("Please enter a valid 10-digit phone number.")
                continue

            customer = Customer(
                customer_id,
                name,
                phone
            )

            customer_manager.add_customer(customer)

        # View Customers
        elif choice == "2":

            customer_manager.view_customers()

        # Search Customer
        elif choice == "3":

            customer_id = input("Enter Customer ID: ")
            customer_manager.search_customer(customer_id)

        # Update Customer
        elif choice == "4":

            customer_id = input("Enter Customer ID: ")
            name = input("Enter New Name: ")
            phone = input("Enter New Phone Number: ")

            if not phone.isdigit() or len(phone) != 10:
                print("Please enter a valid 10-digit phone number.")
                continue

            customer_manager.update_customer(
                customer_id,
                name,
                phone
            )

        # Delete Customer
        elif choice == "5":

            customer_id = input("Enter Customer ID: ")
            customer_manager.delete_customer(customer_id)

        # Back to Main Menu
        elif choice == "6":

            break

        else:

            print("Invalid choice. Please try again.")


def create_sale_menu():

    print("\n===== CREATE SALE =====")

    customer_id = input("Enter Customer ID: ")
    product_id = input("Enter Product ID: ")

    if not customer_id or not product_id:
        print("Customer ID and Product ID cannot be empty.")
        return

    try:
        quantity = int(input("Enter Quantity: "))

    except ValueError:
        print("Please enter a valid number.")
        return

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    sales_manager.create_sale(
        customer_id,
        product_id,
        quantity
    )


def main_menu():

    while True:

        print("\n")
        print("=" * 45)
        print("   SMART SALES & INVENTORY MANAGEMENT")
        print("=" * 45)

        print("1. Product Management")
        print("2. Customer Management")
        print("3. Create Sale")
        print("4. Sales History")
        print("5. Sales Report")
        print("6. Low Stock Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            product_menu()

        elif choice == "2":

            customer_menu()

        elif choice == "3":

            create_sale_menu()

        elif choice == "4":

            sales_manager.view_sales()

        elif choice == "5":

            report_manager.sales_summary()

        elif choice == "6":

            report_manager.low_stock_report()

        elif choice == "7":

            print("Thank you for using the system.")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()