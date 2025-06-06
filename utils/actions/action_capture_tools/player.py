# player.py

import json
import time
import pyautogui
from pynput import mouse

# ——————————————————————————————————————————————
# HELPER FUNCTIONS
# ——————————————————————————————————————————————
def do_hold(pos, duration):
    """
    Move instantly to pos, hold right-click for 'duration' seconds, then release.
    """
    x, y = pos
    pyautogui.moveTo(x, y, duration=0.02)
    pyautogui.mouseDown(button='right')
    time.sleep(duration)
    pyautogui.mouseUp(button='right')


def do_click(pos):
    """
    Move instantly to pos and perform a left-click.
    """
    x, y = pos
    pyautogui.moveTo(x, y, duration=0.02)
    pyautogui.click(button='left')


def do_type(char):
    """
    Type a single character into the active window.
    """
    pyautogui.typewrite(char)


# ——————————————————————————————————————————————
# WAIT FOR RIGHT-CLICK TO START PLAYBACK
# ——————————————————————————————————————————————
start_playback = False

def on_start(x, y, button, pressed):
    """
    As soon as a RIGHT-click press (pressed=True) is detected, stop listening
    and set start_playback=True. That triggers the main loop.
    """
    global start_playback
    if button == mouse.Button.right and pressed:
        start_playback = True
        print("▶️  Right-click detected. Beginning playback in 0.5s...\n")
        return False  # stop listener


if __name__ == "__main__":
    # 1) Load recorded actions from JSON
    fname = "route4_ly_mkt_to_ly_spw.json"
    with open(fname, "r") as f:
        actions = json.load(f)

    # 2) Prompt the user to right-click to begin
    print("▶️  player.py loaded. To start playback, RIGHT-click anywhere.")
    with mouse.Listener(on_click=on_start) as listener:
        listener.join()

    # Slight pause to ensure focus has switched to the game window
    time.sleep(0.5)

    # 3) Replay each recorded action in sequence
    for idx, act in enumerate(actions, start=1):
        pause = act.get("pause_before", 0.0)
        time.sleep(pause)

        if act["action"] == "hold" and act["button"] == "right":
            pos = act["pos"]
            duration = act["duration"]
            do_hold(pos, duration)

        elif act["action"] == "click" and act["button"] == "left":
            pos = act["pos"]
            do_click(pos)

        elif act["action"] == "type":
            ch = act["char"]
            do_type(ch)

        else:
            print(f"⚠️  Skipping unknown action: {act}")

    print("✔️  Playback complete.")
