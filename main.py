from utils.actions.action_capture_tools.player_external import play_route, resolve_route_path, resolve_cta_clicks
from utils.wait.wait import wait_for_right_click
from utils.transition_check.avatar_presence_check import wait_until_avatar_visible
from utils.sheets.sheet_reader import read_items_and_modes_from_sheet
from utils.actions.typing.search_typing import type_item_into_searchbox
from utils.price_reader.value_reader import get_adjusted_price
from utils.sheets.update_cell_writer import write_value_to_cell
import time



city_sequence = ["lymhurst", "bridgewatch", "martlock", "thetford", "fort_sterling", "lymhurst"]
city_sequence = ["thetford", "fort_sterling", "lymhurst"]

if __name__ == "__main__":

    # ---------------------- signal to start
    wait_for_right_click()

    # ---------------------- looping each city
    for i in range(len(city_sequence) - 1):
        city = city_sequence[i]
        next_city = city_sequence[i + 1]

        # ---------------------- spawn to market entry
        resolve_route_path(city, "spawn_to_market")

        # ---------------------- check if zoned in
        time.sleep(5)
        if wait_until_avatar_visible(min_duration=5, timeout = 60):
            print("Ready to proceed.")
        else:
            print("Avatar never stabilized. Check loading or region.")
            exit()

        # ---------------------- entrance to market
        resolve_route_path(city, "market_to_trader")

        # ---------------------- market scanning
        resolve_cta_clicks("set_category")
        
        item_data = read_items_and_modes_from_sheet()
        col_number_map = {
            "lymhurst":3,
            "bridgewatch":4,
            "martlock":5,
            "thetford":6,
            "fort_sterling":7
        }
        col_number = col_number_map[city]

        for idx, entry in enumerate(item_data, start=2):
            item = entry["item"]
            mode = entry["mode"]
            print(f"[{idx}] Typing '{item}' ({mode}) into search box...")
            type_item_into_searchbox(item)
            time.sleep(1)
            resolve_cta_clicks("buy")
            time.sleep(1)
            price = get_adjusted_price(mode)
            row_number = idx
            resolve_cta_clicks("close_buy_modal")
            write_value_to_cell(row_index=row_number, col_index=col_number, value_to_write=price)

        # ---------------------- close market
        resolve_cta_clicks("close_market")

        # ---------------------- market to city
        resolve_route_path(city, "trader_to_city")

        # ---------------------- check if zoned out
        time.sleep(5)
        if wait_until_avatar_visible(min_duration=5, timeout = 60):
            print("Ready to proceed.")
        else:
            print("Avatar never stabilized. Check loading or region.")
            exit()

        # ---------------------- city to travel planner
        resolve_route_path(city, "city_to_travel_planner")

        # ---------------------- select city from dropdown
        resolve_cta_clicks(next_city)

        # ---------------------- buy travel
        resolve_cta_clicks("buy_travel")
        time.sleep(10)

