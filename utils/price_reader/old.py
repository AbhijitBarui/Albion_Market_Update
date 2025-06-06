# value_reader_with_screenshots.py

import time
import re
import pyautogui
import pytesseract
from PIL import Image

# ─── (A) TESSERACT CONFIG ─────────────────────────────────────────────────────────
# If tesseract is not on your PATH, uncomment and set the full path:
# pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"

# ─── (B) SCREEN REGIONS ────────────────────────────────────────────────────────────
# Adjust these so they tightly frame the topmost Sell/Buy price cells:
# SELL_TOP_REGION = (1309, 447, 41, 15)
SELL_TOP_REGION = (2749, 447, 41, 15)
# SELL_TOP_REGION = (0, 0, 1000, 1000)
BUY_TOP_REGION  = (2912, 447, 41, 15)

# ─── (C) OCR HELPER FUNCTION ──────────────────────────────────────────────────────
def read_top_price(region, save_path):
    """
    1) Take a screenshot of `region = (x, y, w, h)` and save it to disk.
    2) Convert to grayscale.
    3) Run pytesseract to extract digits.
    4) Return the first integer found (or None).
    """
    # 1) Screenshot and save
    screenshot: Image.Image = pyautogui.screenshot(region=region)
    screenshot.save(save_path)
    print(f"   • Saved region screenshot to '{save_path}'")

    # 2) Convert to grayscale
    gray = screenshot.convert("L")

    # 3) (Optional) thresholding if OCR is noisy:
    # thresh = gray.point(lambda p: 0 if p < 128 else 255, "1")
    # text = pytesseract.image_to_string(thresh, config="--psm 7 digits")

    # Direct grayscale OCR
    text = pytesseract.image_to_string(gray, config="--psm 7 digits")

    # 4) Extract the first integer
    m = re.search(r"(\d+)", text)
    if m:
        return int(m.group(1))
    else:
        return None


# ─── (D) MAIN BLOCK ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("▶️  Waiting 2 seconds. Make sure the Albion market panel is fully visible.")
    time.sleep(2)

    # Read & save Sell region
    sell_price = read_top_price(SELL_TOP_REGION, "sell_region.png")
    if sell_price is None:
        print("⚠️  Could not read a Sell price from the defined region.")
    else:
        print(f"✅ Top Sell Orders price = {sell_price}")

    # Read & save Buy region
    buy_price = read_top_price(BUY_TOP_REGION, "buy_region.png")
    if buy_price is None:
        print("⚠️  Could not read a Buy price from the defined region.")
    else:
        print(f"✅ Top Buy Orders price  = {buy_price}")

    print("\n✔️  Done. Inspect 'sell_region.png' and 'buy_region.png' to adjust your regions.")
