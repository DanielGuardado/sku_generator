from google_sheets_client import GoogleSheetsClient
from google_api_helper import GoogleAPIHelper

# from db import Database
from config import SPREADSHEET_ID
import os

# from utils import preprocess_data
from barcode_generator import create_pdf


def main():
    service_account_file = "./service_account.json"
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    api_helper = GoogleAPIHelper(service_account_file, scopes)
    creds = api_helper.get_credentials()
    sheets_service = api_helper.get_service("sheets", creds)
    gsheet_client = GoogleSheetsClient(sheets_service, SPREADSHEET_ID)
    auto_generate = input(
        "Do you want to auto-generate SKUs for all hauls without generated SKUs? (Y/N): "
    )
    if auto_generate.upper() == "Y":
        hauls = [
            row["haul_number"]
            for row in gsheet_client.get_all_values("Hauls", "0", "skus_generated")
        ]

    else:
        hauls = input("Enter haul IDs separated by space: ")
        hauls = hauls.upper().split(" ")
    add_upc = input("Do you want to include UPC? (Y/N): ")

    if add_upc.upper() == "Y":
        include_upc = True
    else:
        include_upc = False

    for haul_number in hauls:
        haul_data = gsheet_client.get_all_values("Hauls", haul_number, "haul_number")

        haul_products = gsheet_client.get_all_values("Products", haul_number, "haul_id")
        pdf_path = create_pdf(haul_number, haul_products, include_upc=include_upc)
        if not pdf_path:
            print(
                f"Failed to generate PDF for haul {haul_number}, Please check the logs"
            )
            continue
        os.startfile(pdf_path, "print")
        updated_haul_data = haul_data[0].copy()
        if not include_upc:
            updated_haul_data["skus_generated"] = 1

        updated_row = gsheet_client.update_row("Hauls", updated_haul_data)
        if updated_row:
            print(f"SKU generation status updated for haul {haul_number}")
        else:
            print(f"Failed to update SKU generation status for haul {haul_number}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
