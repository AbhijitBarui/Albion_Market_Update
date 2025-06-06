from pynput import mouse

def wait_for_right_click():
    """
    Blocks until a right-click press is detected. Then exits.
    """
    print("🕐 Waiting for right-click to proceed...")

    def on_click(x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            print("▶️ Right-click detected. Continuing...\n")
            return False  # stop listener

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
