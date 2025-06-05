# avatar_presence_via_text.py

import time
import pytesseract
import pyautogui
from PIL import Image

# ─── (A) CONFIGURATION ───────────────────────────────────────────────────────────

# 1. The region (left_x, top_y, width, height) that tightly encloses the character name.
#    We assume the capitalized name “Operate” lives here in full‐desktop coords:
TEXT_REGION = (2145, 223, 95, 23)

# 2. Poll interval (seconds)
POLL_INTERVAL = 0.5

# 3. Tesseract parameters
#    We’ll use --psm 7 (treat the region as a single line of text) and limit to ASCII letters.
TESSERACT_CONFIG = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# 4. The exact string to look for (case‐insensitive). If you change your character’s name,
#    modify this accordingly (e.g. "MyCharName" or use .lower() on both sides).
TARGET_NAME = "operate"


# ─── (B) OCR‐BASED PRESENCE CHECK ─────────────────────────────────────────────────
def is_avatar_present_by_text():
    """
    1) Take a screenshot of TEXT_REGION.
    2) Run Tesseract on it (grayscale + single line).
    3) Return True if the OCR’d text (lowercase) contains TARGET_NAME, else False.
    """
    # 1) Screenshot the region
    im: Image.Image = pyautogui.screenshot(region=TEXT_REGION)
    gray = im.convert("L")

    # 2) Run Tesseract
    text = pytesseract.image_to_string(gray, config=TESSERACT_CONFIG)
    text = text.strip().lower()

    # 3) Debug: print what OCR returned (uncomment if you want to see every frame)
    # print(f"OCR returned: '{text}'")

    return TARGET_NAME in text


# ─── (C) MAIN LOOP ───────────────────────────────────────────────────────────────
def monitor_avatar_via_text():
    """
    Checks TEXT_REGION every POLL_INTERVAL seconds,
    flags ‘absent’ when TARGET_NAME disappears, and ‘present’ when it reappears.
    """
    print(f"▶️  Starting text‐based avatar monitor (poll every {POLL_INTERVAL}s).")
    print(f"   TEXT_REGION = {TEXT_REGION}, looking for “{TARGET_NAME}”\n")
    print("   Press Ctrl+C to stop.\n")

    # Initial check
    try:
        present = is_avatar_present_by_text()
    except Exception as e:
        print("❌ Error during initial OCR:", e)
        present = False

    state_str = "present" if present else "absent"
    print(f"[{time.strftime('%H:%M:%S')}] Avatar is initially: {state_str}")

    try:
        while True:
            try:
                found = is_avatar_present_by_text()
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] ❌ OCR error: {e}")
                found = False

            # If state changed, print a message
            if found and not present:
                print(f"[{time.strftime('%H:%M:%S')}] ▶️ Avatar has reappeared (text detected).")
                present = True
            elif not found and present:
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Avatar has disappeared (no text).")
                present = False

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n⏹ Monitoring stopped by user. Exiting.")


if __name__ == "__main__":
    monitor_avatar_via_text()
