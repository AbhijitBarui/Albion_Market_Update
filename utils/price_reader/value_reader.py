import re
import pyautogui
import pytesseract
from PIL import Image

# ─── CONFIG ──────────────────────────────────────────────────────────────────────
# Adjust screen coordinates (full-screen resolution assumed)
SELL_TOP_REGION = (2749, 403, 41, 15)
BUY_TOP_REGION  = (2912, 403, 41, 15)

# Tesseract OCR mode (only digits)
OCR_CONFIG = "--psm 7 digits"

def read_price(region):
    """
    Captures screenshot from `region`, applies OCR, and returns the first integer found.
    """
    screenshot: Image.Image = pyautogui.screenshot(region=region)
    gray = screenshot.convert("L")
    text = pytesseract.image_to_string(gray, config=OCR_CONFIG)
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else None

def get_adjusted_price(mode: str):
    """
    Returns adjusted price based on `mode`:
    - If mode is "buy": return top BUY price + 1
    - If mode is "sell": return top SELL price - 1
    """
    mode = mode.lower()
    if mode not in ["buy", "sell"]:
        raise ValueError("Mode must be 'buy' or 'sell'")

    region = BUY_TOP_REGION if mode == "buy" else SELL_TOP_REGION
    raw_price = read_price(region)

    if raw_price is None:
        print(f"⚠️  Could not read a {mode.upper()} price from the screen.")
        return None

    adjusted = raw_price + 1 if mode == "buy" else raw_price - 1
    print(f"✅ Top {mode.upper()} price: {raw_price} → Adjusted: {adjusted}")
    return adjusted
