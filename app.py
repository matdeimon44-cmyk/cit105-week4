import streamlit as st
from datetime import date
from decimal import Decimal

from calculations import calculate_invoice, line_total
from storage import save_invoice, load_invoices
from pdf_export import create_invoice_pdf


st.set_page_config(page_title="Invoice Application", page_icon="🧾")

st.title("🧾 Invoice Application")
st.write("Create, save, reload, and export invoices.")


# -------------------------
# Session state
# -------------------------

if "items" not in st.session_state:
    st.session_state["items"] = []


# -------------------------
# Client information
# -------------------------

st.header("Client Information")

client_name = st.text_input("Client Name")
client_address = st.text_input("Client Address")
invoice_number = st.text_input("Invoice Number")
invoice_date = st.date_input("Invoice Date", value=date.today())


# -------------------------
# Add line item
# -------------------------

st.header("Line Items")

description = st.text_input("Description")

quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=1,
    step=1
)

unit_price = st.number_input(
    "Unit Price",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f"
)

if st.button("Add Item"):
    item_total = line_total(quantity, unit_price)

    st.session_state["items"].append(
        {
            "description": description,
            "quantity": int(quantity),
            "unit_price": str(Decimal(str(unit_price)).quantize(Decimal("0.01"))),
            "line_total": str(item_total),
        }
    )

    st.success("Item added.")


# -------------------------
# Display / remove items
# -------------------------

if st.session_state["items"]:
    st.subheader("Current Items")

    for index, item in enumerate(st.session_state["items"]):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(
                f"{item['description']} | "
                f"Qty: {item['quantity']} | "
                f"${item['unit_price']} | "
                f"Total: ${item['line_total']}"
            )

        with col2:
            if st.button("Remove", key=f"remove_{index}"):
                st.session_state["items"].pop(index)
                st.rerun()


# -------------------------
# Discount and tax
# -------------------------

st.header("Totals")

discount_percent = st.number_input(
    "Discount (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

tax_percent = st.number_input(
    "Tax (%)",
    min_value=0.0,
    value=0.0,
    step=0.1
)

totals = calculate_invoice(
    st.session_state["items"],
    discount_percent,
    tax_percent
)

st.write(f"Subtotal: ${totals['subtotal']}")
st.write(f"Discount: ${totals['discount']}")
st.write(f"Tax: ${totals['tax']}")
st.subheader(f"Grand Total: ${totals['grand_total']}")


# -------------------------
# Build invoice data
# -------------------------

invoice = {
    "client_name": client_name,
    "client_address": client_address,
    "invoice_number": invoice_number,
    "date": str(invoice_date),
    "items": st.session_state["items"],
    "discount_percent": str(discount_percent),
    "tax_percent": str(tax_percent),
    "subtotal": str(totals["subtotal"]),
    "discount": str(totals["discount"]),
    "tax": str(totals["tax"]),
    "grand_total": str(totals["grand_total"]),
}


# -------------------------
# Save invoice
# -------------------------

if st.button("Save Invoice"):
    if not invoice_number:
        st.error("Please enter an invoice number.")
    elif not client_name:
        st.error("Please enter a client name.")
    elif not st.session_state["items"]:
        st.error("Please add at least one item.")
    else:
        save_invoice(invoice)
        st.success("Invoice saved successfully.")


# -------------------------
# PDF export
# -------------------------

pdf_data = create_invoice_pdf(invoice)

st.download_button(
    label="Export Invoice as PDF",
    data=pdf_data,
    file_name=f"invoice_{invoice_number or 'sample'}.pdf",
    mime="application/pdf",
)


# -------------------------
# Saved invoices
# -------------------------

st.header("Saved Invoices")

saved_invoices = load_invoices()

if saved_invoices:
    selected_number = st.selectbox(
        "Previously Saved Invoices",
        [invoice["invoice_number"] for invoice in saved_invoices],
    )

    selected_invoice = next(
        invoice
        for invoice in saved_invoices
        if invoice["invoice_number"] == selected_number
    )

    st.write(
        f"Client: {selected_invoice.get('client_name', '')}"
    )
    st.write(
        f"Grand Total: ${selected_invoice.get('grand_total', '0.00')}"
    )

    saved_pdf = create_invoice_pdf(selected_invoice)

    st.download_button(
        "Download Saved Invoice PDF",
        data=saved_pdf,
        file_name=f"invoice_{selected_number}.pdf",
        mime="application/pdf",
    )

else:
    st.info("No saved invoices yet.")