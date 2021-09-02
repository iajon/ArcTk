import tkinter as tk
from tkinter import ttk

from gui.tabs import Home, ProcessArtifacts

class CustomNotebook(ttk.Notebook):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        self.init_widgets()

    def init_widgets(self):
        # Home Tab
        self.home_tab = Home(self, self.app)
        self.add(self.home_tab, text = "Home")

        # Process Artifacts Tab
        self.process_artifacts_tab = ProcessArtifacts(self, self.app)
        self.add(self.process_artifacts_tab, text = "Process Artifacts")