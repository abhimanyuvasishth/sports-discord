import os
from functools import cache

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()


@cache
def get_sheet(doc_name, sheet_name):
    client = authorize_client()
    return client.open(doc_name).worksheet(sheet_name)


def authorize_client():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
    parsed_dict = {
        "type": os.getenv('GOOGLE_SHEET_CREDENTIAL_TYPE'),
        "project_id": os.getenv('GOOGLE_SHEET_PROJECT_ID'),
        "private_key_id": os.getenv('GOOGLE_SHEET_PRIVATE_KEY_ID'),
        "private_key": os.getenv('GOOGLE_SHEET_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('GOOGLE_SHEET_CLIENT_EMAIL'),
        "client_id": os.getenv('GOOGLE_SHEET_CLIENT_ID'),
        "auth_uri": os.getenv('GOOGLE_SHEET_AUTH_URI'),
        "token_uri": os.getenv('GOOGLE_SHEET_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('GOOGLE_SHEET_AUTH_PROVIDER_CERT_URL'),
        "client_x509_cert_url": os.getenv('GOOGLE_SHEET_CERT_URL')
    }
    creds = Credentials.from_service_account_info(parsed_dict, scopes=scopes)
    return gspread.authorize(creds)
