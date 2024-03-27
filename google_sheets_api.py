class GoogleSheetsClient:
    def __init__(self, service, spreadsheet_id):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def _find_column_index(values, column_name):
        """Find the index of a column by its name in the first row of values."""
        if values and len(values) > 0:
            first_row = values[0]
            if column_name in first_row:
                return first_row.index(column_name)
        return None

    # def get_batch_names(self, sheet_name, haul_id=None):
    #     """Fetches all rows from the specified sheet and filters rows based on a named column."""
    #     range_name = f"{sheet_name}"  # Just the sheet name, no specific range

    #     sheet = self.service.spreadsheets()
    #     result = (
    #         sheet.values()
    #         .get(spreadsheetId=self.spreadsheet_id, range=range_name)
    #         .execute()
    #     )
    #     values = result.get("values", [])

    #     batch_names = []
    #     if not values:
    #         print("No data found.")
    #         return batch_names
    #     else:
    #         # Get the column names from the first row
    #         column_names = values[0]

    #         # Process each row as a dictionary
    #         for row in values[1:]:
    #             row_dict = dict(zip(column_names, row))
    #             if haul_id is None or row_dict.get("haul_id") == haul_id:
    #                 batch_name = {
    #                     "product": row_dict.get("product"),
    #                     "console": row_dict.get("console"),
    #                     "packaging": row_dict.get("packaging"),
    #                     "condition": row_dict.get("condition"),
    #                     "condition_notes": row_dict.get("condition_notes"),
    #                     "inserts": row_dict.get("inserts"),
    #                     "sku": row_dict.get("sku")
    #                 }
    #                 # Only add if 'name' exists in the row
    #                 if batch_name["product"]:
    #                     batch_names.append(batch_name)

    #     return batch_names
    def get_batch_names(self, sheet_name, haul_id=None):
        """Fetches all rows from the specified sheet and filters rows based on a named column."""
        range_name = f"{sheet_name}"  # Just the sheet name, no specific range

        sheet = self.service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.spreadsheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])

        batch_names = []
        if not values:
            print("No data found.")
            return batch_names
        else:
            # Get the column names from the first row
            column_names = values[0]

            # Process each row as a dictionary
            for row in values[1:]:
                row_dict = dict(zip(column_names, row))
                if haul_id is None or row_dict.get("haul_id") == haul_id:
                    batch_name = {
                        "product": row_dict.get("product"),
                        "main_category": row_dict.get("main_category"),
                        "sub_category": row_dict.get("sub_category"),
                        "packaging": row_dict.get("packaging"),
                        "condition": row_dict.get("condition"),
                        "condition_notes": row_dict.get("condition_notes"),
                        "inserts": row_dict.get("inserts"),
                        "sku": row_dict.get("sku"),
                        "upc": row_dict.get("upc"),
                        "list_price": row_dict.get("list_price"),
                        "title_change": row_dict.get("title_change"),
                    }
                    # Only add if 'name' exists in the row
                    if batch_name["product"]:
                        batch_names.append(batch_name)

        return batch_names
