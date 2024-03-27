from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from barcode import generate
from barcode.writer import ImageWriter
import os

def generate_barcodes(data):
    barcode_paths = []
    # Create the directory if it doesn't exist
    if not os.path.exists("barcode_images"):
        os.makedirs("barcode_images")
    for item in data:
        for i in range(2):  # Generate two sets of barcodes for each item
            barcode = generate('code128', item[1], output=os.path.join("barcode_images", f"{item[0]}_{i}"), writer=ImageWriter())
            filename = f"{item[0]}_{i}.png"
            filepath = os.path.join("barcode_images", filename)
            barcode.save(filepath)
            barcode_paths.append(filepath)
    return barcode_paths

def create_pdf(barcode_images, output_file="barcode_sheet.pdf"):
    c = canvas.Canvas(output_file, pagesize=letter)
    x_offset = 50
    y_offset = 750
    row_height = 100
    column_width = 200
    for i, image_path in enumerate(barcode_images):
        if i % 2 == 0 and i != 0:
            x_offset = 50
            y_offset -= row_height
        c.drawImage(image_path, x_offset, y_offset, width=100, height=50)
        x_offset += column_width
    c.save()

if __name__ == "__main__":
    data = [('abc', '123'), ('efg', '456'), ('hij', '789')]
    barcode_images = generate_barcodes(data)
    create_pdf(barcode_images)
    print("Barcode sheet generated successfully.")
