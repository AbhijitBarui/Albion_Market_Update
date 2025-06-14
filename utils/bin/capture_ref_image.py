# capture_avatar_ref_fixed.py

import pyautogui

# ─── (A) FULL‐DESKTOP COORDS FOR AVATAR/NAME‐TAG ────────────────────────────────
# Based on your measurements (632 + 1440, 209, 209, 70):
AVATAR_REGION = (2750, 403, 25, 15)  # (left_x, top_y, width, height)

if __name__ == "__main__":
    # Just grab that exact rectangle and save it as avatar_ref.png
    avatar_crop = pyautogui.screenshot(region=AVATAR_REGION)
    avatar_crop.save("123123123.png")
    print("✅ Saved 'avatar_ref.png' (avatar reference) from region:", AVATAR_REGION)
