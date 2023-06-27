import os
import datetime
import sqlite3
from database import create_database, DATABASE_FILE
from pdf_generator import generate_invoice, validate_customer_id

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_menu():
    print("Electricity Bill Application")
    print("======================================")
    print("1. Add a new customer")
    print("2. Select an existing customer")
    print("3. Generate an invoice")
    print("4. Add index for a specific month")
    print("5. Exit")

# CLI Functionality
def add_customer():
    print("Add a new customer")
    print("==================")
    name = input("Name: ")
    address = input("Address: ")
    index_initial = 0

    while True:
        phone = input("Phone: ")
        if len(phone) != 10:
            print("Error: Phone number must contain 10 digits.")
        else:
            break

    connexion = sqlite3.connect(DATABASE_FILE)
    c = connexion.cursor()

    c.execute("INSERT INTO customers (name, address, phone, index_initial) VALUES (?, ?, ?, ?)",
              (name, address, phone, index_initial))

    connexion.commit()
    connexion.close()

    print("Customer added successfully.")

def add_index():

    print("Add index for a specific month")
    print("==============================")

    connexion = sqlite3.connect(DATABASE_FILE)
    c = connexion.cursor()

    customer_id = input("Customer ID: ")

    try:
        validate_customer_id(customer_id)
        previous_index_final = c.execute("SELECT index_final FROM bills WHERE customer_id = ? ORDER BY id DESC LIMIT 1",
                                         (customer_id,)).fetchone()
        if previous_index_final:
            index_initial = previous_index_final[0]
        else:
            index_initial = c.execute("SELECT index_initial FROM customers WHERE id = ?", (customer_id,)).fetchone()[0]
    except ValueError as e:
        print(f"Error: {str(e)}")
        return

    month = input("Month: ")
    year = input("Year: ")
    index_final = int(input("Index_final: "))
    consumption = index_final - index_initial
    unit_price = input("Unit Price: ")
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO bills (customer_id, month, year, index_initial, index_final, consumption, unit_price, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (customer_id, month, year, index_initial, index_final, consumption, unit_price, date))
    c.execute("UPDATE customers SET index_initial = ? where id = ?", (index_final, customer_id))

    connexion.commit()
    connexion.close()

    print("Index added successfully.")


def main():
    create_database()

    while True:
        clear_screen()
        print_main_menu()
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_customer()

        elif choice == "2":

            try:
                while True:
                    clear_screen()
                    print("Customer Options")
                    print("======================================")
                    print("1. Generate an invoice")
                    print("2. Add index for a specific month")
                    print("3. Go back")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        month = input("Month: ")
                        year = input("Year: ")
                        try:
                            generate_invoice(customer_id, month, year)
                        except ValueError as e:
                            print(f"Error: {str(e)}")
                    elif sub_choice == "2":
                        add_index()
                    elif sub_choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            except ValueError as e:
                print(f"Error: {str(e)}")

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
