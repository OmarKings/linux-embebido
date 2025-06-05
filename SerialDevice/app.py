import os
import yaml
from tkinter import Tk, Frame, TOP, X
from SerialDevice.serial_devices_bar import SerialDevicesBar


class App(Tk):
    def __init__(self, *args, **kwargs):
        # Load configuration before initializing the window
        self.config_data = self.load_config()
        super().__init__(*args, **kwargs)

        # Apply window settings from config
        app_cfg = self.config_data.get('main_app', {})
        title = app_cfg.get('title', 'Serial Device App')
        width = app_cfg.get('width', 800)
        height = app_cfg.get('height', 600)
        icon_path = app_cfg.get('icon')

        self.title(title)
        self.geometry(f"{width}x{height}")
        if icon_path and os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                print(f"Warning: could not load icon '{icon_path}'")

        # Window behavior
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)

        # Initialize the GUI
        self.init_gui()

    def init_gui(self):
        # Top frame for SerialDevicesBar
        top_frame = Frame(self)
        top_frame.pack(side=TOP, fill=X)

        # Instantiate and pack the serial devices bar
        self.serial_devices_bar = SerialDevicesBar(self)
        self.serial_devices_bar.pack(in_=top_frame, side="top", fill="x")
        self.serial_devices_bar.update_serial_devices()

        # Example: add a combobox for selection if needed
        # from tkinter.ttk import Combobox
        # devices = self.serial_devices_bar.get_device_list()
        # self.combo = Combobox(self, values=devices)
        # self.combo.pack(side="top", fill="x", padx=10, pady=5)

        # Placeholder for additional widgets
        # e.g. Buttons, Labels, etc.

    def on_closing(self):
        # Add confirmation dialog logic here if desired
        if self.confirm_exit():
            self.destroy()

    def confirm_exit(self):
        # TODO: Prompt the user with a dialog to confirm exit
        return True

    @staticmethod
    def load_config():
        # Load YAML config file
        cfg_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if not os.path.exists(cfg_path):
            raise FileNotFoundError(f"Configuration file not found: {cfg_path}")
        with open(cfg_path, 'r') as file:
            return yaml.safe_load(file)


if __name__ == "__main__":
    app = App()
    app.mainloop()
