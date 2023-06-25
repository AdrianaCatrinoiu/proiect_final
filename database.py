import os
import sqlite3
from sqlite3 import Error




DATABASE_FILE = "electricity_bills.db"
""" Database Initialization"""

def create_database():
    connexion = sqlite3.connect(DATABASE_FILE)
    c = connexion.cursor()

    # Create customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    index_initial INTEGER NOT NULL)''')

    # Create bills table
    c.execute('''CREATE TABLE IF NOT EXISTS bills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    index_initial INTEGER DEFAULT 0 NOT NULL,
                    index_final INTEGER NOT NULL,
                    consumption INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id))''')
    connexion.commit()
    connexion.close()


def validate_customer_id(customer_id):

    connexion = sqlite3.connect(DATABASE_FILE)
    c = connexion.cursor()

    c.execute("SELECT COUNT(*) FROM customers WHERE id=?", (customer_id,))
    count = c.fetchone()[0]

    connexion.close()

    if count == 0:
        raise ValueError("Invalid customer ID.")
    


def generate_invoice(customer_id, month, year):

    connexion = sqlite3.connect(DATABASE_FILE)
    c = connexion.cursor()

    # Get customer details
    c.execute("SELECT name, address, phone FROM customers WHERE id=?", (customer_id,))
    customer = c.fetchone()

    if not customer:
        connexion.close()
        raise ValueError("Invalid customer ID.")

    # Get consumption details
    c.execute("SELECT index_initial, index_final, consumption, unit_price, date FROM bills WHERE customer_id=? AND month=? AND year=?", (customer_id, month, year))
    consumption_details = c.fetchone()

    if not consumption_details:
        connexion.close()
        raise ValueError("No consumption details found for the specified month and year.")

    connexion.close()

