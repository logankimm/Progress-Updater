import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .google_apis import Google_APIs

class Sheets_API(Google_APIs):
    sheet = None
    SPREADSHEET_ID = None
    SHEET_NAME = None
    START_ROW = 0
    COLUMNS = [("B", "D"), ("F", "H"), ("J", "L"), ("N", "P"), ("R", "T"), ("V", "X"), ("Z", "AB"), ("AD", "AF")]

    def __init__(self, scopes, ID, *args):
        # Super method to create credentials
        try:
            super().__init__(scopes)
        except:
            logging.info("Error while creating instance of Google API")
            raise ValueError

        self.SPREADSHEET_ID = ID

        service = build("sheets", "v4", credentials=self.credentials)
        self.sheet = service.spreadsheets()

        self.get_sheets()
        self.START_ROW = self.get_first_empty_row()

    def get_sheets(self):
        try:
            metadata = self.sheet.get(spreadsheetId=self.SPREADSHEET_ID).execute()
            properties = metadata.get('sheets')
            self.SHEET_NAME = properties[0]['properties']['title']

        except HttpError as err:
            print(err)
        return
    
    def get_first_empty_row(self):
        try:
            # Call the Sheets API
            result = (
                self.sheet.values()
                .get(spreadsheetId=self.SPREADSHEET_ID, range="{}!B:B".format(self.SHEET_NAME))
                .execute()
            )
            values = result.get("values", [])
            return len(values) + 1

        except HttpError as err:
            print(err)

    def update_scenario(self, data, scenario_index, row_index):
        # Update index used based off different scenario
        values = {"values" : data}

        self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID,
            range = "{sheet_name}!{column_start}{row_start}:{column_end}{row_end}".format(
                sheet_name = self.SHEET_NAME,
                column_start = self.COLUMNS[scenario_index][0],
                column_end = self.COLUMNS[scenario_index][1],
                row_start = self.START_ROW,
                row_end = self.START_ROW + row_index),
            valueInputOption = "USER_ENTERED",
            body = values).execute()
        
        return