import serial.tools.list_ports
from tkinter import Frame, Button
from tkinter.ttk import Combobox

class SerialDevicesBar(Frame):
    """
    A top-bar widget listing available serial ports with a refresh button.
    """
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # Combobox for serial ports
        self.combo = Combobox(self, state="readonly")
        self.combo.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # Refresh button
        self.refresh_btn = Button(self, text="Refresh", command=self.update_serial_devices)
        self.refresh_btn.pack(side="right", padx=5, pady=5)

        # Initially load devices
        self.update_serial_devices()

    def update_serial_devices(self):
        """
        Query system for serial ports and update the combobox values.
        """
        ports = serial.tools.list_ports.comports()
        device_list = [port.device for port in ports]
        # Update combobox
        self.combo['values'] = device_list
        if device_list:
            # Select first device by default
            self.combo.current(0)

    def get_selected_device(self):
        """
        Return the currently selected serial port (string) or None if none.
        """
        return self.combo.get() if self.combo.get() else None

    def get_device_list(self):
        """
        Return the full list of available serial ports.
        """
        return list(self.combo['values'])
