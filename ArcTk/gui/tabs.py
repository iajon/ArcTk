import tkinter as tk
from tkinter import ttk

from gui.frames import *

class Home(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        self.init_widgets()
    
    def init_widgets(self):
        # Container for active_box_frame and menu_frame
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill = "both", expand = "True")

        # Active box frame (left)
        self.active_box_frame = ActiveBox(self.container, self.app)
        self.active_box_frame.pack(side = "left", fill = "both", padx = (20, 10), pady = (10, 10), anchor = "nw")
        self.app.widgets['active_box_frame'] = self.active_box_frame

        # Menu Frame (right)
        self.menu_frame = Menu(self.container, self.app)
        self.menu_frame.pack(side = "right", fill = "both", expand = "True", padx = (10, 20), pady = (10, 10), anchor = "ne")
        self.app.widgets['menu_frame'] = self.menu_frame

        # Box tree (bottom)
        self.box_tree_frame = BoxTree(self, self.app)
        self.box_tree_frame.pack(fill="both", expand = "True", padx = (20, 15), pady = (10, 20), anchor = "s")
        self.app.widgets['box_treeview'] = self.box_tree_frame.box_treeview

class ProcessArtifacts(ttk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        self.init_widgets()
    
    def init_widgets(self):
        # Active box frame (top)
        self.small_active_box_frame = SmallActiveBox(self, self.app)
        self.small_active_box_frame.pack(side = "top", fill = "x", expand = "True", padx = 20, pady = (10, 5), anchor = "nw")
        self.app.widgets['small_active_box_frame'] = self.small_active_box_frame

        # Container for container_2 and container_3
        self.container_1 = ttk.Frame(self)
        self.container_1.pack(anchor = 'nw')

        # Container for bag_entry_frame and artifact_entry_frame
        self.container_2 = ttk.Frame(self.container_1)
        self.container_2.pack(side="left", anchor = 'nw')

        # Container for card_preview_frame and submit_button
        self.container_3 = ttk.Frame(self.container_1)
        self.container_3.pack(side = "right", fill = "both", expand = "True", anchor = 'nw')

        # Bag entry frame 
        self.bag_entry_frame = BagEntry(self.container_2, self.app)
        self.bag_entry_frame.pack(padx = (20, 15), pady = (0, 5), anchor = 'nw')
        self.app.widgets['bag_entry_frame'] = self.bag_entry_frame

        # Artifact entry frame 
        self.artifact_entry_frame = ArtifactEntry(self.container_2, self.app)
        self.artifact_entry_frame.pack(fill = "both", expand = "True", padx = (20, 15), pady = (0, 10), anchor = 'nw')
        self.app.widgets['artifact_entry_frame'] = self.artifact_entry_frame

        # Card preview frame
        self.card_preview_frame = CardPreview(self.container_3, self.app)
        self.card_preview_frame.pack(side = "top", padx = (0, 20), anchor = 'ne')
        self.app.widgets['card_preview_frame'] = self.card_preview_frame

        # Submit button frame
        self.submit_button_frame = SubmitButton(self.container_3, self.app)
        self.submit_button_frame.pack(fill = "both", expand = "True", padx = (0, 20), pady = (5, 10), anchor = 'ne')
        self.app.widgets['submit_button'] = self.submit_button_frame

        #Bag Treeview (bottom)
        self.bag_tree_frame = BagTree(self, self.app)
        self.bag_tree_frame.pack(side="bottom", fill="x", padx = (20, 15), pady = (5, 20), anchor = "w")
        self.app.widgets['bag_treeview'] = self.bag_tree_frame.bag_treeview

    def submit(self):
        pass
