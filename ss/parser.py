import re
from datetime import date

from ss.connector import SsConnector


class Parser:
    """
    Parses Google Spreadsheet for useful data
    """

    def __init__(self):
        self.ss_connector = SsConnector()
        self.worksheet = self.ss_connector.get_worksheet()

    @staticmethod
    def get_today_date():
        d = date.today()
        return d.strftime('%d.%m')

    def find_birthday_rows(self):
        today = self.get_today_date()
        patter = f"^{today}"
        criteria_re = re.compile(patter)
        cell_list = self.worksheet.findall(criteria_re, in_column=11)  # get data from column K
        return [cell.row for cell in cell_list]

    def parse(self):
        rows = self.find_birthday_rows()
        birthday_guys = list()
        for row in rows:
            try:
                name = self.worksheet.get(f'A{row}')[0][0]  # get() returns list of lists
            except IndexError:
                name = None
            try:
                tg = self.worksheet.get(f'G{row}')[0][0]
            except IndexError:
                tg = None
            birthday_guys.append((name, tg))
        return birthday_guys
