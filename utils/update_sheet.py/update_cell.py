# update_sample_cell.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ─── (A) GOOGLE SHEETS SETUP ─────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = "automationautoapply-4aecae51d1a8.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
gc = gspread.authorize(creds)
sheet = gc.open("ProfitSheets").sheet1

# ─── (B) PARAMETERS ───────────────────────────────────────────────────────────────
row_index = 3       # e.g. “Cotton” is on sheet row 3
col_index = 3       # column 3 corresponds to “Lymhurst”
value_to_write = 1  # sample value

# ─── (C) UPDATE THAT CELL ─────────────────────────────────────────────────────────
sheet.update_cell(row_index, col_index, value_to_write)
print(f"✅ Wrote {value_to_write} into row {row_index}, column {col_index}.")
