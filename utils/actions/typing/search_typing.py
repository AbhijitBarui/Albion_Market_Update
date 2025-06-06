# utils/actions/typing/search_typing.py

import time
import pyautogui

SEARCH_BOX_COORDS = (2515, 385)
PAUSE_AFTER_CLICK = 0.3
TYPING_INTERVAL = 0.08

def type_item_into_searchbox(item_name):
    pyautogui.moveTo(SEARCH_BOX_COORDS, duration=0.05)
    pyautogui.click()
    time.sleep(PAUSE_AFTER_CLICK)
    pyautogui.typewrite(item_name, interval=TYPING_INTERVAL)
    pyautogui.press("enter")
    time.sleep(0.5)
