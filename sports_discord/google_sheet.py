import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet(doc_name, sheet_name):
    client = get_client()
    return client.open(doc_name).worksheet(sheet_name)


def get_client():
    file_name = 'credentials.json'
    scopes = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scopes)
    return gspread.authorize(creds)
