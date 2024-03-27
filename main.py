import os
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import win32print
import win32ui
from PIL import Image, ImageWin


# Function to generate a single barcode
def generate_barcode(sku, width, height):
    barcode_class = barcode.get_barcode_class("code128")
    bc = barcode_class(sku, writer=ImageWriter())
    barcode_image = bc.render(writer_options={"quiet_zone": 1.0})
    return barcode_image.resize((width, height))


# Function to create barcode pages
def create_barcode_pages(
    skus,
    output_folder,
    haul_id,
    page_width,
    page_height,
    barcode_width,
    barcode_height,
    num_cols,
    left_margin,
    space_between,
):
    os.makedirs(output_folder, exist_ok=True)
    max_barcodes_per_col = (page_height - barcode_height) // barcode_height
    max_barcodes_per_page = num_cols * max_barcodes_per_col
    file_paths = []

    for page_num, start in enumerate(range(0, len(skus), max_barcodes_per_page), 1):
        page = Image.new("RGB", (page_width, page_height), "white")
        x_offset = left_margin
        y_offset = 0
        page_skus = skus[start : start + max_barcodes_per_page]

        for sku in page_skus:
            barcode_image = generate_barcode(sku, barcode_width, barcode_height)
            page.paste(barcode_image, (x_offset, y_offset))
            x_offset += barcode_width + space_between
            if x_offset + barcode_width > page_width - left_margin:
                x_offset = left_margin
                y_offset += barcode_height
                if y_offset + barcode_height > page_height:
                    y_offset = 0

        output_file = os.path.join(output_folder, f"{haul_id}_page_{page_num}.png")
        page.save(output_file)
        file_paths.append(output_file)

    return file_paths


# Function to print an image
def print_image(file_path):
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    printer_info = win32print.GetPrinter(hprinter, 2)
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(printer_name)
    pdc.StartDoc(file_path)
    pdc.StartPage()

    bmp = Image.open(file_path)
    dib = ImageWin.Dib(bmp)

    # Get printer resolution
    printer_res_x = pdc.GetDeviceCaps(8)  # HORZRES
    printer_res_y = pdc.GetDeviceCaps(10)  # VERTRES

    # Calculate the scaling factor to fit the image to the page
    scale_x = printer_res_x / bmp.size[0]
    scale_y = printer_res_y / bmp.size[1]
    scale = min(scale_x, scale_y)

    # Calculate the new size of the image
    new_size = (int(bmp.size[0] * scale), int(bmp.size[1] * scale))

    # Calculate the position to center the image
    pos_x = (printer_res_x - new_size[0]) // 2
    pos_y = (printer_res_y - new_size[1]) // 2

    dib.draw(
        pdc.GetHandleOutput(), (pos_x, pos_y, pos_x + new_size[0], pos_y + new_size[1])
    )

    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()


# User inputs
print("sku_generator")
haul_id = input("Enter haul ID: ")
num_skus = int(input("Enter the number of SKUs to generate: "))

# Generating SKUs
skus = [f"{haul_id}{i:03}" for i in range(1, num_skus + 1)]

# A4 size in pixels at 300 DPI
page_width, page_height = 2480, 3508
barcode_width, barcode_height = int(2.42 * 300), 300  # 2.42 inches x 1 inch at 300 DPI

# Parameters
num_cols = 3
left_margin = 100
space_between = 40
output_folder = "barcodes"

# Generating barcode pages
output_file_paths = create_barcode_pages(
    skus,
    output_folder,
    haul_id,
    page_width,
    page_height,
    barcode_width,
    barcode_height,
    num_cols,
    left_margin,
    space_between,
)
for file_path in output_file_paths:
    print_image(file_path)
