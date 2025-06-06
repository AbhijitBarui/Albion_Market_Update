# utils/sheets/update_cell_writer.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ─── (A) GOOGLE SHEETS SETUP ─────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = "credentials/automationautoapply-4aecae51d1a8.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate once
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
gc = gspread.authorize(creds)
sheet = gc.open("ProfitSheets").sheet1

# ─── (B) EXPORTABLE FUNCTION ─────────────────────────────────────────────────────
def write_value_to_cell(row_index, col_index, value_to_write):
    """
    Updates a single cell in the Google Sheet based on provided row, column, and value.
    """
    sheet.update_cell(row_index, col_index, value_to_write)
    print(f"✅ Wrote {value_to_write} into row {row_index}, column {col_index}.")
