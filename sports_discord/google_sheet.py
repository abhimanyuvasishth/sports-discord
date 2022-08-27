from functools import cache

import gspread
import json
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()


@cache
def get_sheet(doc_name, sheet_name):
    client = authorize_client()
    return client.open(doc_name).worksheet(sheet_name)


def authorize_client():
    scopes = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
    ]
    parsed_dict = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(parsed_dict, scopes)
    return gspread.authorize(creds)
