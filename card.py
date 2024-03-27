import barcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

# Define a single product for testing
product = {
    "product": "LEGO The Hobbit",
    "condition": "brand new",
    "title_change": "Brand New Damaged",
    "list_price": "15.99",
    "sku": "EB056001",
}


def generate_barcode(sku, file_format="png"):
    code = barcode.get("code128", sku, writer=barcode.writer.ImageWriter())
    return code.save(sku)


def wrap_text(text, max_width, font_name, font_size):
    words = text.split()
    wrapped_text = ""
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            wrapped_text += f"{line}\n"
            line = word
    wrapped_text += line  # Add the last line
    return wrapped_text


def create_card(c, product, x, y, card_width, card_height):
    font_name = "Helvetica"
    font_size = 10
    padding = 5 * mm

    barcode_height = 25 * mm
    barcode_filename = generate_barcode(product["sku"])

    # Draw the barcode image at the top of the card
    c.drawImage(
        barcode_filename,
        x + padding,
        y - barcode_height,
        width=80 * mm,
        height=barcode_height,
    )

    y_text_start = y - barcode_height - padding
    text_max_width = card_width - (2 * padding)

    keys_to_create = ["product", "condition", "title_change", "list_price"]

    for key in keys_to_create:
        value = product.get(key, "")
        wrapped_text = wrap_text(
            f"{key.replace('_', ' ').title()}: {value}",
            text_max_width,
            font_name,
            font_size,
        )
        for line in wrapped_text.split("\n"):
            c.drawString(x + padding, y_text_start, line)
            y_text_start -= font_size * 1.5  # Adjust line height


def create_pdf(product):
    c = canvas.Canvas("product_card.pdf", pagesize=letter)
    width, height = letter

    card_width = width / 3
    card_height = height / 5

    x = 0  # Start at the left edge of the paper
    y = height  # Start at the top edge of the paper

    create_card(c, product, x, y, card_width, card_height)

    c.showPage()
    c.save()


create_pdf(product)
