from __future__ import print_function

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# CONSTANTS
SCOPES = ["https://www.googleapis.com/auth/drive"]
folder_id = "16EYX3ruxgAYlisaqH10OaCwUVm07m5mJ"
m_type = {
    "csv": "text/csv",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def authorize():
    creds = None
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "service_credentials.json", SCOPES
    )
    return creds


creds = authorize()

service = build("drive", "v3", credentials=creds)


def save_to_drive(filename, mime):
    media = MediaFileUpload(
        filename,
        mimetype=m_type[mime],
        resumable=True,
    )

    try:
        old_file_id = (
            service.files()
            .list(q=f"mimeType='{m_type[mime]}' and trashed=false")
            .execute()["files"][0]["id"]
        )

        file = (
            service.files()
            .update(fileId=old_file_id, media_body=media, fields="id")
            .execute()
        )

    except IndexError:
        file_metadata = {"name": filename, "parents": [folder_id]}
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )