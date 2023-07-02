from pathlib import Path
import sqlite3
from fpdf import FPDF
from database import DATABASE_PATH


def validate_customer_id(customer_id):
    """Validates customer ID if it exists in the customers table."""

    connexion = sqlite3.connect(str(DATABASE_PATH))
    c = connexion.cursor()

    c.execute("SELECT COUNT(*) FROM customers WHERE id=?", (customer_id,))
    count = c.fetchone()[0]

    connexion.close()

    if count == 0:
        raise ValueError("Invalid customer ID.")
    

def generate_invoice(customer_id, month, year):
    """Generate an invoice as a PDF file for a specific customer, month, and year."""

    connexion = sqlite3.connect(str(DATABASE_PATH))
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

    # Generate PDF invoice
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Invoice", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, txt=f"Customer Name: {customer[0]}", ln=True)
    pdf.cell(0, 10, txt=f"Address: {customer[1]}", ln=True)
    pdf.cell(0, 10, txt=f"Phone: {customer[2]}", ln=True, align="L")
    pdf.ln(10)

    # Table
    pdf.set_font("Arial", "B", 12)
    pdf.cell(30, 10, "Period", border=1)
    pdf.cell(30, 10, "Unit Price", border=1)
    pdf.cell(30, 10, "Index Initial", border=1)
    pdf.cell(30, 10, "Index End", border=1)
    pdf.cell(30, 10, "Consum", border=1)
    pdf.cell(30, 10, "Total Amount", border=1)
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(30, 10,  txt=f"{year}_{month}", border=1)
    pdf.cell(30, 10, str(consumption_details[3]), border=1)
    pdf.cell(30, 10, str(consumption_details[0]), border=1)
    pdf.cell(30, 10, str(consumption_details[1]), border=1)
    pdf.cell(30, 10, str(consumption_details[2]), border=1)
    pdf.cell(30, 10, str(consumption_details[2]*consumption_details[3]), border=1)
    
    pdf.ln(50)
    pdf.cell(0, 10, txt=f"Date Generated Invoice: {consumption_details[4]}", ln=True)

    
    invoice_dir = Path(__file__).resolve().parent / "invoices"
    invoice_dir.mkdir(exist_ok=True)
    invoice_filename = f"Invoice_{customer_id}_{month}_{year}.pdf"
    invoice_path = invoice_dir / invoice_filename

    pdf.output(str(invoice_path))

    print(f"Invoice generated successfully: {invoice_path}")
