import json
from pathlib import Path


DATA_FILE = Path("invoices.json")


def save_invoice(invoice):
    """Save an invoice to the JSON file."""
    invoices = load_invoices()
    invoices.append(invoice)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(invoices, file, indent=4)


def load_invoices():
    """Load all previously saved invoices."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def get_invoice(invoice_number):
    """Find an invoice by its invoice number."""
    invoices = load_invoices()

    for invoice in invoices:
        if str(invoice.get("invoice_number")) == str(invoice_number):
            return invoice

    return None
