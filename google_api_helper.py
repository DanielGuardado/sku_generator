from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleAPIHelper:
    def __init__(self, service_account_file, scopes):
        self.service_account_file = service_account_file
        self.scopes = scopes

    def get_credentials(self):
        """Retrieve Google API credentials."""
        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes
        )
        return creds

    def get_service(self, service_type, creds):
        """Build a Google API service client."""
        if service_type == "drive":
            return build("drive", "v3", credentials=creds)
        elif service_type == "sheets":
            return build("sheets", "v4", credentials=creds)
        else:
            raise ValueError("Unsupported service type")
