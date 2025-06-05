# recorder.py

import json
import time
from pynput import mouse, keyboard

# ——————————————————————————————————————————————
# GLOBALS
# ——————————————————————————————————————————————
events = []
last_event_time = None

# For tracking a right-click “hold”
right_start_time = None
right_start_pos = None

# Flag to indicate that recording has officially started
started = False

# ——————————————————————————————————————————————
# CALLBACKS
# ——————————————————————————————————————————————
def on_click(x, y, button, pressed):
    """
    1) The very first right-button press (pressed=True) sets 'started = True' 
       and initializes last_event_time, but does NOT record anything.
    2) Once started, every right-click hold (press→release) and 
       every left-click release will be recorded, along with pause timings.
    """
    global right_start_time, right_start_pos, last_event_time, started

    now = time.time()

    # If this is the first right-click press, start recording from here
    if button == mouse.Button.right and pressed and not started:
        started = True
        last_event_time = now
        print("▶️  First right-click detected. Recording has started.")
        return

    # If we haven't started yet, ignore everything else
    if not started:
        return

    # ---- once started=True, handle holds and clicks exactly as before ----
    # Right-click pressed: mark the start time/position for the hold
    if button == mouse.Button.right and pressed:
        right_start_time = now
        right_start_pos = (x, y)
        return

    # Right-click released: record the hold event
    if button == mouse.Button.right and not pressed:
        if right_start_time is None:
            return  # safety check
        duration = round(now - right_start_time, 3)

        pause_before = round(right_start_time - last_event_time, 3) if last_event_time else 0.0

        events.append({
            "action": "hold",
            "button": "right",
            "pos": [right_start_pos[0], right_start_pos[1]],
            "duration": duration,
            "pause_before": pause_before
        })

        print(f"Recorded HOLD → offset: {right_start_pos}, duration: {duration}s, pause_before: {pause_before}s")

        last_event_time = now
        right_start_time = None
        right_start_pos = None
        return

    # Left-click released: record a click event
    if button == mouse.Button.left and not pressed:
        pause_before = round(now - last_event_time, 3) if last_event_time else 0.0

        events.append({
            "action": "click",
            "button": "left",
            "pos": [x, y],
            "pause_before": pause_before
        })

        print(f"Recorded CLICK → pos: ({x}, {y}), pause_before: {pause_before}s")

        last_event_time = now
        return


def on_press(key):
    """
    Once started=True, record every printable key press as a 'type' event.
    Ignite pause timing from last_event_time.
    """
    global last_event_time, started

    if not started:
        return

    try:
        char = key.char  # only single-character keys
    except AttributeError:
        return

    now = time.time()
    pause_before = round(now - last_event_time, 3) if last_event_time else 0.0

    events.append({
        "action": "type",
        "char": char,
        "pause_before": pause_before
    })

    print(f"Recorded TYPE → '{char}', pause_before: {pause_before}s")

    last_event_time = now


# ——————————————————————————————————————————————
# MAIN
# ——————————————————————————————————————————————
if __name__ == "__main__":
    print("▶️  recorder.py loaded. To begin recording, perform a RIGHT-click anywhere.")
    print("▶️  After the first right-click, every right HOLD (press+release), left click, and typing will be recorded.")
    print("▶️  Press Ctrl+C to stop and save.\n")

    with mouse.Listener(on_click=on_click) as mouse_listener, \
         keyboard.Listener(on_press=on_press) as key_listener:
        try:
            mouse_listener.join()
        except KeyboardInterrupt:
            pass

    if events:
        filename = "route.json"
        with open(filename, "w") as f:
            json.dump(events, f, indent=2)
        print(f"\n✔️  Recording stopped. {len(events)} events saved to '{filename}'.")
    else:
        print("\n⚠️  Recording stopped. No events were captured.")
