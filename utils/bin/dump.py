# dump_avatar_region.py

import pyautogui
import time

# The region you believe contains your avatar + name‐tag on the external monitor:
AVATAR_REGION = (2072, 209, 209, 70)  # (left_x, top_y, width, height)

print("▶️  Waiting 2 seconds—make sure Albion is visible on the external monitor.")
time.sleep(2)

# Take a screenshot of exactly that box:
crop = pyautogui.screenshot(region=AVATAR_REGION)
crop.save("avatar_region_dump.png")
print(f"✅ Saved screenshot of AVATAR_REGION to 'avatar_region_dump.png' (region = {AVATAR_REGION})")
