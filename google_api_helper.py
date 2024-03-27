import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleAPIHelper:
    def __init__(self, token_file, credentials_file, scopes):
        self.token_file = token_file
        self.credentials_file = credentials_file
        self.scopes = scopes

    def get_credentials(self):
        """Retrieve Google API credentials."""
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_file, "wb") as token:
                pickle.dump(creds, token)

        return creds

    def get_service(self, service_type, creds):
        """Build a Google API service client."""
        if service_type == "drive":
            return build("drive", "v3", credentials=creds)
        elif service_type == "sheets":
            return build("sheets", "v4", credentials=creds)
        else:
            raise ValueError("Unsupported service type")
