from pathlib import Path
import sqlite3


DATABASE_PATH = Path("electricity_bills.db")

""" Database Initialization"""

def create_database():
    """Create the SQLite database and the required tables if they don't exist."""
    connexion = sqlite3.connect(DATABASE_PATH)
    c = connexion.cursor()

    # Create customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    index_initial INTEGER NOT NULL
                    )''')

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

