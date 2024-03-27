import io
from googleapiclient.http import MediaIoBaseUpload


class GoogleDriveClient:
    def __init__(self, service):
        self.service = service

    def create_folder(self, name, parent_id=None):
        """Create a folder in Google Drive."""
        file_metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            file_metadata["parents"] = [parent_id]

        folder = self.service.files().create(body=file_metadata, fields="id").execute()
        print(f"Folder created with ID: {folder.get('id')}")
        return folder.get("id")

    def find_folder(self, name, parent_id=None):
        """Check if a folder exists in Google Drive and return its ID."""
        # Escape single quotes in the name
        escaped_name = name.replace("'", "\\'")

        query = f"name = '{escaped_name}' and mimeType = 'application/vnd.google-apps.folder'"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        response = (
            self.service.files()
            .list(q=query, spaces="drive", fields="files(id, name)", pageSize=10)
            .execute()
        )

        for file in response.get("files", []):
            # Assuming first match is the desired one
            print(f"Found folder: {file.get('name')} with ID: {file.get('id')}")
            return file.get("id")

        print(f"No folder found with name: {name}")
        return None

    def create_text_file(self, name, content, parent_id=None):
        """Create a text file in Google Drive with the given content."""
        file_metadata = {"name": name, "mimeType": "text/plain"}

        if parent_id:
            file_metadata["parents"] = [parent_id]

        # Encode the content to bytes, prepare it for upload
        content_bytes = content.encode("utf-8")
        media = MediaIoBaseUpload(
            io.BytesIO(content_bytes), mimetype="text/plain", resumable=True
        )

        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        print(f"Text file created with ID: {file.get('id')}")
        return file.get("id")
