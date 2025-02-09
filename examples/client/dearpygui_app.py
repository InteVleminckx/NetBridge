from netbridge.client.api import connect, get_state, update_state
import dearpygui.dearpygui as dpg
import time
import threading
import json

class DearPyGuiUI:
    def __init__(self):
        self.client = None
        self.running = True  # Flag to control the main loop

    @connect
    def setup(self, client):
        self.client = client

        # Set up the Dear PyGui window
        self.setup_window()

        # Start Dear PyGui in the main thread
        self.run_dearpygui()

    def setup_window(self):
        dpg.create_context()
        dpg.create_viewport(title="Dear PyGui Window", width=300, height=200)
        dpg.setup_dearpygui()

        with dpg.window(label="Square Controller", width=280, height=180):
            dpg.add_text("Enter X and Y coordinates:")
            dpg.add_input_int(tag="input_x", label="X", default_value=100, min_value=0, max_value=750)
            dpg.add_input_int(tag="input_y", label="Y", default_value=100, min_value=0, max_value=550)
            dpg.add_button(label="Add Square", callback=self.add_square_callback)
            dpg.add_button(label="Stop pygame", callback=self.stop_pygame_callback)
            dpg.add_text("FPS: 0", tag="fps_text")

    def update_fps(self):

        data, info = get_state(self.client)
        if not data:
            return

        dpg.set_value("fps_text", f"FPS: {data['fps']:.0f}")

    def run_dearpygui(self):
        dpg.show_viewport()
        while dpg.is_dearpygui_running() and self.running:
            self.update_fps()
            dpg.render_dearpygui_frame()
        self.running = False
        dpg.destroy_context()

    def add_square_callback(self):
        x = dpg.get_value("input_x")
        y = dpg.get_value("input_y")

        data = {
            "squares": [(x, y)]
        }
        
        success, info = update_state(self.client, data)

    def stop_pygame_callback(self):

        data = {"running": False}
        
        succeed, info = update_state(self.client, data)


if __name__ == "__main__":
    app = DearPyGuiUI()

    # Run the setup
    app.setup()
