import tkinter as tk
from tkinter import ttk

import sqlite3 as sl

from gui.frames import *
from gui.notebooks import *
from gui.tabs import *
from gui.windows import AdditionalToolsWindow

from events import EventManager

from sql.queries import Connection

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Theme
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "light")
        self.title("ArcTk")

        self.event_manager = EventManager(self)
        self.connection = Connection('database.db')
        self.widgets = {}

        self.init_widgets()
    
    def init_widgets(self):
        c1 = CustomNotebook(self, self)
        c1.pack(side="top", fill="both", padx = 10, pady = 10)

        a1 = AdditionalToolsWindow(self)


if __name__ == "__main__":
    app = App()

    app.mainloop()