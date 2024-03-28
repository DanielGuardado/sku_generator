import barcode
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Your product data here in the 'products' list


def generate_barcode(haul_id, sku, barcode_type, file_format="png"):
    base_dir = os.path.join(".", "haul_ids", haul_id)
    sub_dir = os.path.join(base_dir, barcode_type)  # 'sku' or 'price' subfolder
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)  # Create the directory if it does not exist

    code = barcode.get("code128", sku, writer=barcode.writer.ImageWriter())
    file_name = sku.replace(".", "-") + "." + file_format
    barcode_path = os.path.join(sub_dir, file_name)
    barcode_file = code.save(
        barcode_path
    )  # Save the barcode image in the specific subfolder

    return barcode_file


def create_pdf(
    haul_id,
    products,
    products_per_row=3,
    rows_per_page=5,
    font_name="Helvetica",
    font_size=8,
):
    base_dir = os.path.join(".", "haul_ids", haul_id)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    pdf_path = os.path.join(base_dir, "product_barcodes.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter  # Width and height of the paper

    card_width = width / products_per_row
    card_height = height / rows_per_page

    c.setFont(font_name, font_size)

    # Adjust barcode size
    barcode_width = 40 * mm
    barcode_height = 12 * mm

    for index, product in enumerate(products):
        col = index % products_per_row
        row = index // products_per_row % rows_per_page

        x = col * card_width
        y = height - ((row + 1) * card_height)

        # Calculate positions
        barcode_x = x + (card_width - barcode_width) / 3
        top_barcode_y = y + card_height - barcode_height - 5 * mm

        # Generate and draw the barcode for SKU
        sku_barcode_filename = generate_barcode(haul_id, product["sku"], "sku")
        c.drawImage(
            sku_barcode_filename,
            barcode_x,
            top_barcode_y,
            width=barcode_width,
            height=barcode_height,
        )

        # Generate and draw the barcode for list price
        price_barcode_filename = generate_barcode(
            haul_id, product["list_price"], "price"
        )
        bottom_barcode_y = top_barcode_y - barcode_height - 5 * mm

        c.drawImage(
            price_barcode_filename,
            barcode_x,
            bottom_barcode_y,
            width=barcode_width,
            height=barcode_height,
        )

        # Position for the key-value pairs
        text_x = x + 10 * mm
        text_y = bottom_barcode_y - font_size * 2

        # Draw the key-value pairs
        for key in ["product", "condition", "title_change", "list_price"]:
            value = product.get(key, "")
            truncated_value = (value[:20] + "...") if len(value) > 20 else value
            text_line = f"{key.replace('_', ' ').title()}: {truncated_value}"
            c.drawString(text_x, text_y, text_line)
            text_y -= font_size * 1.2

        # Check if we need to start a new page
        if (index + 1) % (products_per_row * rows_per_page) == 0 and index + 1 != len(
            products
        ):
            c.showPage()

    c.save()
    return pdf_path  # Return the file path of the generated PDF
