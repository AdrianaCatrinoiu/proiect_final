from function import add_customer,add_index,handle_customer_options
from database import create_database, DATABASE_PATH
from pdf_generator import generate_invoice,validate_customer_id


def print_main_menu():
    print("Electricity Bill Application")
    print("======================================")
    print("1. Add a new customer")
    print("2. Select an existing customer")
    print("3. Generate an invoice")
    print("4. Add index for a specific month")
    print("5. Exit")


def main():
    """Main function to run the electricity bill application."""

    create_database()

    while True:
       
        print_main_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_customer()

        elif choice == "2":
            handle_customer_options()
           
        elif choice == "3":
            customer_id = input("Customer ID: ")
            month = input("Month: ")
            year = input("Year: ")

            try:
                validate_customer_id(customer_id)
                generate_invoice(customer_id, month, year)
            except ValueError as e:
                print(f"Error: {str(e)}")
        elif choice == "4":
            add_index()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Exiting the program.")
if __name__ == "__main__":
    main()



 
