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
    products_per_row=4,
    rows_per_page=5,
    font_name="Helvetica",
    font_size=8,
    include_upc=False,
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
    barcode_height = 11.5 * mm

    for index, product in enumerate(products):
        if (
            product["sku"] is None
            or product["condition"] is None
            or product["list_price"] is None
        ):
            print(f"Missing data for product {product['product']}")
            return False
        if (
            (product["sku"] == "")
            or (product["condition"] == "")
            or (product["list_price"] == "")
        ):
            print(f"Missing data for product {product['product']}")
            return False

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
        bottom_barcode_y = top_barcode_y - barcode_height - 2 * mm

        # generate and draw the barcode for the upc

        c.drawImage(
            price_barcode_filename,
            barcode_x,
            bottom_barcode_y,
            width=barcode_width,
            height=barcode_height,
        )

        # Position for the key-value pairs
        text_x = x + 10 * mm
        # if include_upc_item:
        #     text_y = bottom_bottom_barcode_y - font_size * 2
        # else:
        text_y = bottom_barcode_y - font_size * 1.3

        # Draw the key-value pairs
        for key in [
            "product",
            "condition",
            "sub_category",
        ]:
            value = product.get(key, "")
            # split the value if it is too long

            if value is not None:
                truncated_value = (value[:20] + "...") if len(value) > 20 else value
            else:
                truncated_value = ""
            # text_line = f"{key.replace('_', ' ').title()}: {truncated_value}"
            if key == "product":
                text_line_top = value[:20]
                text_line_bottom = value[20:]
                c.drawString(text_x, text_y, text_line_top)
                text_y -= font_size * 1
                if len(text_line_bottom) > 0:
                    c.drawString(text_x, text_y, text_line_bottom)
                    text_y -= font_size * 1
            else:
                text_line = value
                c.drawString(text_x, text_y, text_line)
                text_y -= font_size * 1
            # Draw UPC barcode
        include_upc_item = include_upc and product.get("upc") != ""
        if include_upc_item:
            upc_barcode_filename = generate_barcode(haul_id, product["upc"], "upc")
            bottom_bottom_barcode_y = text_y - barcode_height - 0 * mm
            c.drawImage(
                upc_barcode_filename,
                barcode_x,
                bottom_bottom_barcode_y,
                width=barcode_width,
                height=barcode_height,
            )
            text_y = (
                bottom_bottom_barcode_y - font_size * 1
            )  # Adjust text_y for the next iteration
        # Check if we need to start a new page
        if (index + 1) % (products_per_row * rows_per_page) == 0 and index + 1 != len(
            products
        ):
            c.showPage()
            c.setFont(font_name, font_size)

    c.save()
    return pdf_path  # Return the file path of the generated PDF
