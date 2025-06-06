# utils/sheets/sheet_reader.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_FILE = "credentials/automationautoapply-4aecae51d1a8.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def read_items_and_modes_from_sheet(sheet_name="ProfitSheets"):
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
    gc = gspread.authorize(creds)
    sheet = gc.open(sheet_name).sheet1

    items = sheet.col_values(1)[1:]  # Column A — item names
    modes = sheet.col_values(2)[1:]  # Column B — buy/sell

    if len(items) != len(modes):
        raise ValueError(f"Mismatched rows: {len(items)} items vs {len(modes)} modes")

    return [
        {"item": itm.strip(), "mode": mode.strip().lower()}
        for itm, mode in zip(items, modes)
        if itm.strip() and mode.strip()
    ]
