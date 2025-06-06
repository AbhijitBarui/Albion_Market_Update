import json
import time
import pyautogui
from pynput import mouse

# —————————————————————————————————————————
# HELPER FUNCTIONS
# —————————————————————————————————————————
def do_hold(pos, duration):
    x, y = pos
    pyautogui.moveTo(x, y, duration=0.02)
    pyautogui.mouseDown(button='right')
    time.sleep(duration)
    pyautogui.mouseUp(button='right')

def do_click(pos):
    x, y = pos
    pyautogui.moveTo(x, y, duration=0.02)
    pyautogui.click(button='left')

def do_type(char):
    pyautogui.typewrite(char)

# —————————————————————————————————————————
# MAIN FUNCTION
# —————————————————————————————————————————
def play_route(json_path):
    """
    Starts playback of the given JSON action route.
    """
    print(f"\n▶️  player.py loaded with: {json_path}")

    # Wait for right-click to trigger start
    start_playback = True
    # def on_start(x, y, button, pressed):
    #     nonlocal start_playback
    #     if button == mouse.Button.right and pressed:
    #         start_playback = True
    #         print("▶️  Right-click detected. Beginning playback in 0.5s...\n")
    #         return False  # stop listener

    # with mouse.Listener(on_click=on_start) as listener:
    #     listener.join()

    time.sleep(0.5)

    with open(json_path, "r") as f:
        actions = json.load(f)

    for idx, act in enumerate(actions, start=1):
        time.sleep(act.get("pause_before", 0.0))

        if act["action"] == "hold" and act["button"] == "right":
            do_hold(act["pos"], act["duration"])

        elif act["action"] == "click" and act["button"] == "left":
            do_click(act["pos"])

        elif act["action"] == "type":
            do_type(act["char"])

        else:
            print(f"⚠️  Skipping unknown action: {act}")
    
        print("✔️  Playback complete.")

    # Final cleanup to prevent unintended character movement
    pyautogui.mouseUp(button='right')
    pyautogui.moveTo(100, 100, duration=0.05)

    print("✔️  Playback complete.")


# —————————————————————————————————————————
# ROUTE RESOLVER (city + type → path)
# —————————————————————————————————————————
def resolve_route_path(city, route_type):
    route_map = {
        "spawn_to_market": "route1",
        "market_to_trader": "route2",
        "trader_to_city": "route3",
        "city_to_travel_planner": "route4"
    }
    route_prefix = route_map.get(route_type)

    city_acr_map = {
        "lymhurst": "ly",
        "bridgewatch": "bw",
        "fort_sterling": "fs",
        "thetford": "tf",
        "martlock": "ml",
    }
    city_prefix = city_acr_map.get(city)

    if not route_prefix:
        raise ValueError(f"Unknown route_type: {route_type}")

    # return f"utils/actions/movements/{city}/{route_prefix}_{city_prefix}.json"
    path = f"utils/actions/movements/{city}/{route_prefix}_{city_prefix}.json"
    play_route(path)

def resolve_cta_clicks(action_type):
    action_map = {
        "bridgewatch": "choose_city_from_dropdown/bw",
        "fort_sterling": "choose_city_from_dropdown/fs",
        "thetford": "choose_city_from_dropdown/tf",
        "martlock": "choose_city_from_dropdown/ml",
        "lymhurst": "choose_city_from_dropdown/ly",
        "close_market": "close_market/close_market",
        "buy": "hit_buy/hit_buy",
        "set_category": "set_category/choose_category_resource",
        "buy_travel": "buy_travel/buy_travel",
        "close_buy_modal": "close_buy_modal/close_buy_modal"
    }
    action_path = action_map.get(action_type)

    if not action_path:
        raise ValueError(f"Unknown action_type: {action_type}")

    # return f"utils/actions/clicks/{action_path}.json"
    path = f"utils/actions/clicks/{action_path}.json"
    play_route(path)


# —————————————————————————————————————————
# EXAMPLE USAGE (Uncomment to run directly)
# —————————————————————————————————————————
# if __name__ == "__main__":
#     path = resolve_route_path("lymhurst", "spawn_to_market")
#     play_route(path)
