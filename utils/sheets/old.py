# sheet_and_type.py

import time
import pyautogui
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ─── (A) GOOGLE SHEET SETUP ───────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = "automationautoapply-4aecae51d1a8.json"
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
gc = gspread.authorize(creds)
sheet = gc.open("ProfitSheets").sheet1

# Read Column A (item names) and Column B (buy/sell) — skip header row
items = sheet.col_values(1)[1:]   # e.g. ["Rugged Hide", "Thin Hide", ...]
modes = sheet.col_values(2)[1:]   # e.g. ["buy", "buy", "sell", ...]

if len(items) != len(modes):
    raise ValueError(
        f"Column A has {len(items)} rows but column B has {len(modes)} rows (after header)."
    )

# Build a list of dicts: { "row": <sheet_row>, "item": <name>, "mode": <buy/sell> }
sheet_data = []
for idx, (itm, m) in enumerate(zip(items, modes), start=2):
    sheet_data.append({
        "row":  idx,
        "item": itm.strip(),
        "mode": m.strip().lower()
    })

# ─── (B) SEARCH‐BOX COORDINATES & TYPING SETTINGS ─────────────────────────────────
# Paste here the exact X, Y screen coordinates of your market‐search input field:
SEARCH_BOX_COORDS = (2515, 385)

# How long to wait after clicking into the search box before typing
PAUSE_AFTER_CLICK = 0.3  # seconds

# Interval between each character when typing (makes it look like “natural” key presses)
TYPING_INTERVAL = 0.08  # seconds

# ─── (C) MAIN LOOP: FOR EACH ITEM → CLICK+TYPE → “ENTER” ─────────────────────────
print("▶️  Make sure your Albion Online market window (search box visible) is active.")
time.sleep(2)  # give you a moment to click back into the game window if needed

for entry in sheet_data:
    row_index = entry["row"]
    item_name = entry["item"]
    mode = entry["mode"]  # “buy” or “sell”
    print(f"\n→ Row {row_index}: Typing '{item_name}' (mode={mode}) into search box")

    # 1) Move cursor into the search‐box & click to focus it
    pyautogui.moveTo(SEARCH_BOX_COORDS[0], SEARCH_BOX_COORDS[1], duration=0.05)
    pyautogui.click()
    time.sleep(PAUSE_AFTER_CLICK)

    # 2) (Optional) Clear any previous text by selecting all and backspacing:
    #    Uncomment these two lines if you find leftover text from the last search.
    # pyautogui.hotkey("ctrl", "a")
    # pyautogui.press("backspace")
    # time.sleep(0.1)

    # 3) Type the item name letter‐by‐letter
    pyautogui.typewrite(item_name, interval=TYPING_INTERVAL)

    # 4) Press ENTER to execute the search
    pyautogui.press("enter")

    # 5) Pause briefly so the market results can load before your next action
    time.sleep(0.5)
    

print("\n✔️  Done typing every item into the search box.")
