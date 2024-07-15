class GoogleSheetsClient:
    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def get_all_values(self, sheet_name, filter_value=None, filter_column_name=None):
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=sheet_name)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            return []

        # Get headers to use as keys for the dictionaries
        header_dict = self.get_headers(values)

        # Create a list of dictionaries for all rows
        data_dict_list = [
            {
                header: row[index] if index < len(row) else None
                for header, index in header_dict.items()
            }
            for row in values[1:]
        ]

        if filter_value is not None and filter_column_name is not None:
            # Find the index of the filter column name
            filter_column_index = header_dict.get(filter_column_name)
            if filter_column_index is not None:
                # Filter rows based on the filter_value and filter_column_index
                filtered_data_dict_list = [
                    row_dict
                    for row_dict in data_dict_list
                    if row_dict.get(filter_column_name) == filter_value
                ]
                return filtered_data_dict_list

        return data_dict_list

    @staticmethod
    def get_headers(values):
        """Get the headers from the first row of the provided values and store them as key-value pairs."""
        if not values or len(values) == 0:
            return {}

        headers = values[0]
        header_dict = {header: index for index, header in enumerate(headers)}
        return header_dict

    def update_row(self, sheet_name, row_data):
        # Fetch the latest values from the sheet
        all_data = self.get_all_values(sheet_name)

        if not all_data:
            raise ValueError("Sheet data is empty or not found.")

        # Get headers from the sheet data
        header_dict = self.get_headers([list(all_data[0].keys())])

        # Find the row index with the matching haul_id
        haul_id = row_data["haul_id"]
        for row_index, row in enumerate(all_data):
            if row["haul_id"] == haul_id:
                # Create the range to update
                range_to_update = f"{sheet_name}!A{row_index + 2}:{chr(65 + len(header_dict) - 1)}{row_index + 2}"
                # Convert the updated row back to a list
                updated_row = [row_data.get(header, "") for header in header_dict]

                # Update the row in Google Sheets
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_to_update,
                    valueInputOption="RAW",
                    body={"values": [updated_row]},
                ).execute()
                return True

        raise ValueError(f"haul_id {haul_id} not found in provided data")
