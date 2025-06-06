import re
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

OCR_CONFIG = "--psm 7 -c tessedit_char_whitelist=0123456789"

# ─── CONFIG ──────────────────────────────────────────────────────────────────────
SELL_TOP_REGION = (2746, 403, 45, 15)
BUY_TOP_REGION  = (2912, 403, 41, 15)


def read_price(region, debug=True):
    """
    Captures screenshot from `region`, enhances image, applies OCR,
    and returns the first integer found. Optionally saves debug images.
    """
    # 1. Screenshot and grayscale
    screenshot = pyautogui.screenshot(region=region).convert("L")

    # 2. Upscale by 4x
    upscale = screenshot.resize((screenshot.width * 4, screenshot.height * 4), Image.LANCZOS)

    # 3. Sharpen + contrast boost
    sharpened = upscale.filter(ImageFilter.SHARPEN)
    contrast = ImageEnhance.Contrast(sharpened).enhance(3.0)

    # 4. Binarize and convert to grayscale again
    threshold = 140
    binary_bw = contrast.point(lambda x: 255 if x > threshold else 0, mode='1')
    binary = binary_bw.convert("L")  # Ensure it's in correct mode for Tesseract

    # 5. Debug output
    if debug:
        screenshot.save("debug_raw.png")
        upscale.save("debug_upscaled.png")
        contrast.save("debug_contrast.png")
        binary.save("debug_binary.png")

    # 6. OCR
    text = pytesseract.image_to_string(binary, config=OCR_CONFIG)
    print(f"OCR Text Output: {repr(text)}")  # Debug log

    # 7. Extract digits
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
