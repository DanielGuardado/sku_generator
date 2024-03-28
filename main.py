from google_sheets_api import GoogleSheetsClient
from google_api_helper import GoogleAPIHelper
from google_drive_api import GoogleDriveClient
from config import (
    SPREADSHEET_ID,
    SHEET_SCOPES,
)

# from db_manager import get_data, insert_data, get_inserted_skus
from barcode_generator import create_pdf
import os


def initialize_clients():
    api_helper = GoogleAPIHelper("token.pickle", "credentials.json", SHEET_SCOPES)
    creds = api_helper.get_credentials()
    drive_service = api_helper.get_service("drive", creds)
    sheets_service = api_helper.get_service("sheets", creds)
    gsheet_client = GoogleSheetsClient(sheets_service, SPREADSHEET_ID)
    gdrive_client = GoogleDriveClient(drive_service)
    return gsheet_client, gdrive_client


def main():
    print("Initializing Google Sheets and Google Drive clients...")
    gsheet_client, gdrive_client = initialize_clients()
    print("Clients initialized successfully.")
    haul_ids = input("Enter haul IDs separated by space: ")
    # how to uppercase the input
    # haul_ids = haul_ids.upper()
    haul_ids = haul_ids.upper().split(" ")
    for haul_id in haul_ids:
        haul_data = gsheet_client.get_batch_names("MainInventoryRework", haul_id)
        pdf_path = create_pdf(haul_id, haul_data)
        # os.startfile(pdf_path, "print")

        print(haul_data)


if __name__ == "__main__":
    main()
