from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_invoice_pdf(invoice):
    """Create a printable PDF invoice and return it as bytes."""
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "INVOICE")
    y -= 35

    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        50, y, f"Invoice Number: {invoice.get('invoice_number', '')}"
    )
    y -= 20

    pdf.drawString(
        50, y, f"Date: {invoice.get('date', '')}"
    )
    y -= 20

    pdf.drawString(
        50, y, f"Client: {invoice.get('client_name', '')}"
    )
    y -= 20

    pdf.drawString(
        50, y, f"Address: {invoice.get('client_address', '')}"
    )
    y -= 35

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Description")
    pdf.drawString(300, y, "Qty")
    pdf.drawString(350, y, "Price")
    pdf.drawString(450, y, "Total")
    y -= 20

    pdf.setFont("Helvetica", 10)

    for item in invoice.get("items", []):
        description = str(item.get("description", ""))
        quantity = item.get("quantity", 0)
        price = item.get("unit_price", "0.00")
        total = item.get("line_total", "0.00")

        pdf.drawString(50, y, description[:35])
        pdf.drawString(300, y, str(quantity))
        pdf.drawString(350, y, f"${price}")
        pdf.drawString(450, y, f"${total}")

        y -= 18

    y -= 15

    pdf.drawString(
        350, y, f"Subtotal: ${invoice.get('subtotal', '0.00')}"
    )
    y -= 18

    pdf.drawString(
        350, y, f"Discount: ${invoice.get('discount', '0.00')}"
    )
    y -= 18

    pdf.drawString(
        350, y, f"Tax: ${invoice.get('tax', '0.00')}"
    )
    y -= 18

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(
        350, y, f"Grand Total: ${invoice.get('grand_total', '0.00')}"
    )

    pdf.save()

    buffer.seek(0)
    return buffer.getvalue()
