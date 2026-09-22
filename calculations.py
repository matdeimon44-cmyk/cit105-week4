from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def money(value):
    """Convert a value to Decimal and round it to cents."""
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(quantity, unit_price):
    """Calculate the total for one invoice line."""
    return money(Decimal(str(quantity)) * Decimal(str(unit_price)))


def calculate_invoice(items, discount_percent=0, tax_percent=0):
    """Calculate subtotal, discount, tax, and grand total."""
    subtotal = sum(
        (line_total(item["quantity"], item["unit_price"]) for item in items),
        Decimal("0.00"),
    )

    discount_rate = Decimal(str(discount_percent)) / Decimal("100")
    tax_rate = Decimal(str(tax_percent)) / Decimal("100")

    discount = money(subtotal * discount_rate)
    taxable_amount = subtotal - discount
    tax = money(taxable_amount * tax_rate)
    grand_total = money(taxable_amount + tax)

    return {
        "subtotal": money(subtotal),
        "discount": discount,
        "tax": tax,
        "grand_total": grand_total,
    }
