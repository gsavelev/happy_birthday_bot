import os

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


class SsConnector:
    """
    Connects Google Drive to read data from Google Spreadsheet
    """
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive']
        self.service_account_file = 'creds/g_key.json'
        self.ss_id = os.getenv('SS_ID')
        self.sheet_name = 'информация'

    def _get_authorized_gs(self):
        g_key_file = os.path.join(os.path.dirname(__file__),
                                  os.pardir, 'creds/g_key.json')
        if os.path.exists(g_key_file):
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                g_key_file, self.scopes)
        else:
            raise FileNotFoundError('Did not find the Google key file')
        self.gc = gspread.authorize(self.credentials)
        return self.gc

    def get_worksheet(self):
        # https://docs.gspread.org/en/latest/index.html
        gc = self._get_authorized_gs()
        sheet = gc.open_by_key(self.ss_id)
        worksheet = sheet.worksheet(self.sheet_name)
        return worksheet
