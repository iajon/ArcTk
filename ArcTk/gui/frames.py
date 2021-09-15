import tkinter as tk
from tkinter import ttk
import pandas as pd
import random

from lib.auto import *
from lib.Classes import Artifact, Bag, Box
from lib.PdfFunctions import PdfFile
import lib.ExcelFunctions as xlf
from gui.treeview import BoxView, BagView



class Menu(ttk.LabelFrame):
    def __init__(self, parent, app, text = "Utilities"):
        super().__init__(parent, text = text)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.pdf_counter = 0

        self.init_widgets()
    
    def init_widgets(self):
        self.set_active_box_button = ttk.Button(self, text="Set Active Box", command = self.set_active)
        self.add_new_box_button = ttk.Button(self, text="Add New Box (+)", command = self.add_new)
        self.export_box_data_button = ttk.Button(self, text="Export Box Data", command = self.export, style = "Accent.TButton")
        self.additional_tools_button = ttk.Button(self, text="Artifact Tools Window", command = self.additional_tools)

        self.additional_tools_button.pack(padx = 20, pady = (12, 5), fill = "both", expand = "True")
        self.set_active_box_button.pack(padx = 20, pady = (5, 5), fill = "both", expand = "True")
        self.add_new_box_button.pack(padx = 20, pady = 5, fill = "both", expand = "True")
        self.export_box_data_button.pack(padx = 20, pady = (5, 5), fill = "both", expand = "True")

    def set_active(self):
        self.em.initialize("set_active_box_window")

    def add_new(self):
        self.em.initialize("box_entry_window")

    def export(self):
        self.em.initialize("export_box_window")
    
    def additional_tools(self):
        self.em.initialize("additional_tools_window")
        
class ActiveBox(ttk.LabelFrame):
    def __init__(self, parent, app, text = "Active Box"):
        super().__init__(parent, text = text)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.init_widgets()
    
    def init_widgets(self):
        # Labels
        self.state_name = ttk.Label(self, text="State", justify = tk.RIGHT)
        self.county_name = ttk.Label(self, text="County", justify = tk.RIGHT)

        self.site_num = ttk.Label(self, text="Site Number", justify = tk.RIGHT)
        self.site_name = ttk.Label(self, text="Site Name", justify = tk.RIGHT)
        self.oin = ttk.Label(self, text="Old Inventory\nNumber(s)", justify = tk.RIGHT)
        self.snum = ttk.Label(self, text="Shelving Number", justify = tk.RIGHT)
        self.inum = ttk.Label(self, text="Ident. Number", justify = tk.RIGHT)
        
        self.collectors = ttk.Label(self, text="Collectors", justify = tk.RIGHT)
        self.years = ttk.Label(self, text="Years", justify = tk.RIGHT)
        self.pname = ttk.Label(self, text="Project Name", justify = tk.RIGHT)
        self.ptype = ttk.Label(self, text="Project Type", justify = tk.RIGHT)
        self.contract = ttk.Label(self, text="Contract No.", justify = tk.RIGHT)

        # Labels to grid
        self.state_name.grid(row = 0, column = 0, padx=(10, 10), pady = (5, 5), sticky='e')
        self.county_name.grid(row = 0, column = 2, padx=(10, 10), pady = (5, 5), sticky='e')

        self.site_num.grid(row = 1, column = 0, padx=(10, 10), pady = (5, 5), sticky='e')
        self.site_name.grid(row = 2, column = 0, padx=(10, 10), pady = (5, 5), sticky='e')
        self.oin.grid(row = 3, column = 0, padx=(10, 10), pady = (0, 0), sticky='e')
        self.snum.grid(row = 4, column = 0, padx=(10, 10), pady = (5, 5), sticky='e')
        self.inum.grid(row = 5, column = 0, padx=(10, 10), pady = (5, 5), sticky='e')

        self.collectors.grid(row = 1, column = 2, padx=(10, 10), pady = (5, 5), sticky='e')
        self.years.grid(row = 2, column = 2, padx=(10, 10), pady = (5, 5), sticky='e')
        self.pname.grid(row = 3, column = 2, padx=(10, 10), pady = (5, 5), sticky='e')
        self.ptype.grid(row = 4, column = 2, padx=(10, 10), pady = (5, 5), sticky='e')
        self.contract.grid(row = 5, column = 2, padx=(10, 10), pady = (5, 10), sticky='e')

        # Entries
        self.state_entry = ttk.Entry(self)
        self.county_entry = ttk.Entry(self)

        self.site_num_entry = ttk.Entry(self)
        self.site_name_entry = ttk.Entry(self)
        self.oin_entry = ttk.Entry(self)
        self.snum_entry = ttk.Entry(self)
        self.inum_entry = ttk.Entry(self)

        self.collectors_entry = ttk.Entry(self)
        self.years_entry = ttk.Entry(self)
        self.pname_entry = ttk.Entry(self)
        self.ptype_entry = ttk.Entry(self)
        self.contract_entry = ttk.Entry(self)

        # Entries to grid
        self.state_entry.grid(row = 0, column = 1,  padx=(10, 10), pady = (5, 5))
        self.county_entry.grid(row = 0, column = 3,  padx=(10, 10), pady = (5, 5))

        self.site_num_entry.grid(row = 1, column = 1,  padx=(10, 10), pady = (5, 5))
        self.site_name_entry.grid(row = 2, column = 1,  padx=(10, 10), pady = (5, 5))
        self.oin_entry.grid(row = 3, column = 1,  padx=(10, 10), pady = (5, 5))
        self.snum_entry.grid(row = 4, column = 1,  padx=(10, 10), pady = (5, 5))
        self.inum_entry.grid(row = 5, column = 1,  padx=(10, 10), pady = (5, 10))

        self.collectors_entry.grid(row = 1, column = 3,  padx=(10, 10), pady = (5, 5))
        self.years_entry.grid(row = 2, column = 3,  padx=(10, 10), pady = (5, 5))
        self.pname_entry.grid(row = 3, column = 3,  padx=(10, 10), pady = (5, 5))
        self.ptype_entry.grid(row = 4, column = 3,  padx=(10, 10), pady = (5, 5))
        self.contract_entry.grid(row = 5, column = 3,  padx=(10, 10), pady = (5, 10))

        # Entries to list
        self.entry_ls = []
        self.entry_ls.append(self.state_entry)
        self.entry_ls.append(self.county_entry)

        self.entry_ls.append(self.site_num_entry)
        self.entry_ls.append(self.site_name_entry)
        self.entry_ls.append(self.oin_entry)
        self.entry_ls.append(self.snum_entry)
        self.entry_ls.append(self.inum_entry)

        self.entry_ls.append(self.collectors_entry)
        self.entry_ls.append(self.years_entry)
        self.entry_ls.append(self.pname_entry)
        self.entry_ls.append(self.ptype_entry)
        self.entry_ls.append(self.contract_entry)

        # Separators
        self.separator = ttk.Separator(self)
        self.separator.grid(row = 6, column = 0, columnspan = 4, padx = 10, sticky = 'ew')

        # Buttons
        self.edit_button = ttk.Button(self, text="Edit Box Info...", command = self.edit)
        self.submit_button = ttk.Button(self, text="Submit Edits", command = self.submit, style="Accent.TButton")
        self.cancel_button = ttk.Button(self, text="Cancel", command = self.refresh)
        
        self.edit_button.grid(row=7, column=0, columnspan = 4, padx = 150, pady = (15, 10), sticky="nsew")

        self.fill_labels()
        
    def edit(self):
        # Enable entries
        self.enable()

        # Remove edit button
        self.edit_button.grid_forget()

        # Pack submit and cancel buttons
        self.submit_button.grid(row=7, column=0, columnspan = 4, padx = 150, pady = (15, 10), sticky="nsew")
        self.cancel_button.grid(row=7, column=3, padx = (0, 10), pady = (15, 10), sticky="nse")

    def refresh(self):
        # Remove edit and submit buttons
        self.submit_button.grid_forget()
        self.cancel_button.grid_forget()

        # Re-initialize in case entry text was edited by user (wipe edits)
        self.init_widgets()
        
    def submit(self):

        # Copy entry values to new list
        ls = []
        for i in self.entry_ls:
            ls.append(i.get())

        # Insert list to dict
        dict = {'site_num' : ls[2],
                'site_name' : ls[3],
                'oin' : ls[4],
                'shelving_num' : ls[5],
                'id_num' : ls[6],
                'collectors' : ls[7],
                'years' : ls[8],
                'pname' : ls[9],
                'ptype' : ls[10],
                'contract' : ls[11]}

        # Generate box from dict
        box = Box(**dict)

        # Submit box
        self.con.update_box(box, target = "active")

        # Update other active box view
        self.em.refresh("small_active_box_frame")
        self.em.refresh("box_treeview")
        self.em.refresh("card_preview_frame")

        self.refresh()

    def fill_labels(self):
        # Get active box data

        try:
            selection = self.con.get_box(target = "active")[0]

            # Insert data into entries
            for i, j in zip(self.entry_ls, selection):
                i.delete(0, tk.END)
                i.insert(0, str(j))
        except:
            print("Failed")

        # Disable entries
        self.disable()

    def disable(self):
        for i in self.entry_ls:
            i['state'] = 'disabled'

    def enable(self):
        for i in self.entry_ls[2:]:
            i['state'] = 'enabled'

class SmallActiveBox(ttk.LabelFrame):
    def __init__(self, parent, app, text = "Active Box"):
        super().__init__(parent, text = text)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.init_widgets()

    def init_widgets(self):
        # Labels
        self.site_num = ttk.Label(self, text="Site Number", justify = tk.RIGHT)
        self.site_name = ttk.Label(self, text="Site Name", justify = tk.RIGHT)
        self.oin = ttk.Label(self, text="Old Inventory\nNumber(s)", justify = tk.RIGHT)
        self.snum = ttk.Label(self, text="Shelving Number", justify = tk.RIGHT)

        self.collectors = ttk.Label(self, text="Collectors", justify = tk.RIGHT)
        self.years = ttk.Label(self, text="Years", justify = tk.RIGHT)
        self.pname = ttk.Label(self, text="Project Name", justify = tk.RIGHT)
        self.ptype = ttk.Label(self, text="Project Type", justify = tk.RIGHT)
        
        # Labels to grid
        self.site_num.grid(row = 0, column = 0, padx=(10, 10), pady = (5, 0), sticky='e')
        self.site_name.grid(row = 0, column = 2, padx=(10, 10), pady = (5, 0), sticky='e')
        self.oin.grid(row = 0, column = 4, padx=(10, 10), pady = (5, 0), sticky='e')
        self.snum.grid(row = 0, column = 6, padx=(10, 10), pady = (10, 10), sticky='e')

        self.collectors.grid(row = 1, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')
        self.years.grid(row = 1, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')
        self.pname.grid(row = 1, column = 4, padx=(10, 10), pady = (10, 10), sticky='e')
        self.ptype.grid(row = 1, column = 6, padx=(10, 10), pady = (10, 10), sticky='e')

        # Entries
        self.site_num_entry = ttk.Entry(self, width = 20)
        self.site_name_entry = ttk.Entry(self, width = 20)
        self.oin_entry = ttk.Entry(self, width = 20)
        self.snum_entry = ttk.Entry(self, width = 20)

        self.collectors_entry = ttk.Entry(self, width = 20)
        self.years_entry = ttk.Entry(self, width = 20)
        self.pname_entry = ttk.Entry(self, width = 20)
        self.ptype_entry = ttk.Entry(self, width = 20)


        # Entries to grid
        self.site_num_entry.grid(row = 0, column = 1,  padx=(10, 10), pady = (5, 0))
        self.site_name_entry.grid(row = 0, column = 3,  padx=(10, 10), pady = (5, 0))
        self.oin_entry.grid(row = 0, column = 5,  padx=(10, 10), pady = (5, 0))
        self.snum_entry.grid(row = 0, column = 7,  padx=(10, 10), pady = (5, 0))

        self.collectors_entry.grid(row = 1, column = 1,  padx=(10, 10), pady = (10, 10))
        self.years_entry.grid(row = 1, column = 3,  padx=(10, 10), pady = (10, 10))
        self.pname_entry.grid(row = 1, column = 5,  padx=(10, 10), pady = (10, 10))
        self.ptype_entry.grid(row = 1, column = 7,  padx=(10, 10), pady = (10, 10))

        # Entry list
        self.entry_ls = []

        self.entry_ls.append(self.site_num_entry)
        self.entry_ls.append(self.site_name_entry)
        self.entry_ls.append(self.oin_entry)
        self.entry_ls.append(self.snum_entry)

        self.entry_ls.append(self.collectors_entry)
        self.entry_ls.append(self.years_entry)
        self.entry_ls.append(self.pname_entry)
        self.entry_ls.append(self.ptype_entry)

        self.fill_labels()

    def fill_labels(self):
        # Get active box data
        try:
            selection = self.con.get_box(target = "active")[0]
            
            # Insert data into entries
            for i, j in zip(self.entry_ls, selection[2:6] + selection[7:11]):
                i.delete(0, tk.END)
                i.insert(0, str(j))
        except:
            pass
        # Disable entries
        self.disable()
        
    def disable(self):
        for i in self.entry_ls:
            i['state'] = 'disabled'

    def refresh(self):
        self.init_widgets()

    def get(self):
        ls = []
        for i in self.entry_ls:
            ls.append(i.get())
        return ls

class BoxTree(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        self.init_widgets()

    def init_widgets(self):
        self.scrollbar = ttk.Scrollbar(self)
        self.box_treeview = BoxView(self, self.app, selectmode="browse", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.box_treeview.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.box_treeview.pack(side="left", fill = "both")

class BagTree(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        self.init_widgets()

    def init_widgets(self):
        self.scrollbar = ttk.Scrollbar(self)
        self.bag_treeview = BagView(self, self.app, selectmode="browse", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.bag_treeview.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.bag_treeview.pack(side="bottom")
    
class BagEntry(ttk.LabelFrame):
    def __init__(self, parent, app, text = "Bag Information"):
        super().__init__(parent, text = text)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.init_widgets()

    def init_widgets(self):
        # Labels
        self.provenience_label = ttk.Label(self, text="Provenience", justify = tk.RIGHT)
        self.cat_num_label = ttk.Label(self, text="Catalogue\nNumber(s)", justify = tk.RIGHT)
        self.other_label = ttk.Label(self, text="Other Labels", justify = tk.RIGHT)
        self.name_label = ttk.Label(self, text="Name(s)", justify = tk.RIGHT)
        self.date_label = ttk.Label(self, text="Date(s)", justify = tk.RIGHT)
        
        self.provenience_label.grid(row = 0, column = 0, padx=(10, 10), pady = (5, 10), sticky='e')
        self.cat_num_label.grid(row = 0, column = 4, padx=(10, 10), pady = (5, 10), sticky='e')

        self.other_label.grid(row = 1, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')
        self.name_label.grid(row = 1, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')
        self.date_label.grid(row = 1, column = 4, padx=(10, 10), pady = (10, 10), sticky='e')

        # Entries
        self.provenience_entry = ttk.Entry(self, width = 55)
        self.cat_num_entry = ttk.Entry(self)
        self.other_entry = ttk.Entry(self)
        self.name_entry = ttk.Entry(self)
        self.date_entry = ttk.Entry(self)

        self.provenience_entry.grid(row = 0, column = 1, columnspan = 3, padx=(10, 10), pady = (5, 10))
        self.cat_num_entry.grid(row = 0, column = 5,  padx=(10, 10), pady = (5, 10))

        self.other_entry.grid(row = 1, column = 1,  padx=(10, 10), pady = (10, 10))
        self.name_entry.grid(row = 1, column = 3,  padx=(10, 10), pady = (10, 10))
        self.date_entry.grid(row = 1, column = 5,  padx=(10, 10), pady = (10, 10))

        self.entry_ls = []
        self.entry_ls.append(self.provenience_entry)
        self.entry_ls.append(self.cat_num_entry)
        self.entry_ls.append(self.other_entry)
        self.entry_ls.append(self.name_entry)
        self.entry_ls.append(self.date_entry)

        #Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=5, column=0, columnspan = 6, padx = 10, sticky="ew")

        #Options label
        self.options_label = ttk.Label(self, text="Options:", justify = tk.RIGHT)
        self.options_label.grid(row = 6, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')

        #Holdover Checkbutton
        self.holdover_var = tk.IntVar(self)
        self.holdover_var.set(0)
        self.holdover_switch = ttk.Checkbutton(self, text="Preserve Entries", variable = self.holdover_var)
        self.holdover_switch.grid(row = 6, column = 1, padx = (10, 10), pady = (10, 10), sticky="ew")

        # Buttons
        self.send_to_card = ttk.Button(self, text="Add to Card Preview", command = self.to_card)
        self.send_to_card.grid(row = 6, column=5, padx = 10, pady = (10, 10), sticky="nsew")

    def to_card(self):
        # Get data from entries
        data = self.get_data()

        # Send data to card
        self.em.set("card_preview_frame", side = "front", dataset = data)

        # Wipe entries
        if not self.holdover_var.get():
            self.wipe()
        else:
            self.holdover_var.set(0)

    def get_data(self):
        bag_dict = {'prov':str(self.entry_ls[0].get()),
                    'cat_num':str(self.entry_ls[1].get()),
                    'other':str(self.entry_ls[2].get()),
                    'name':str(self.entry_ls[3].get()),
                    'date':str(self.entry_ls[4].get())}
        return bag_dict

    def set(self, id = 0):
        data = self.con.get_bag_by_id(id)

        for i, j in zip(self.entry_ls, data):
            i.delete(0, tk.END)
            i.insert(0, j)
        self.holdover_var.set(1)
        self.to_card()

    def wipe(self):
        if self.holdover_var == 1:
            pass
        else:
            for i in self.entry_ls:
                i.delete(0, 'end')

class ArtifactEntry(ttk.LabelFrame):
    def __init__(self, parent, app, text = "Artifact Information"):
        super().__init__(parent, text = text)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        #Autocomplete list
        self.test_list = ('Empty', 'Debitage', 'Utilized Debitage', 'Biface', 'Hafted Biface - Side Notch', 'Hafted Biface - Corner Notch', 'Hafted Biface - Basal Notch', 'Hafted Biface - Stemmed', 'Hafted Biface - Lanceolate', 'Axe', 'Adze', 'Core', 'Drill', 'Uniface', 'Misc. Chipped Stone', 'Groundstone', 'Abrader', 'Mano', 'Metate', 'Nuttingstone', 'Hammerstone', 'Hematite', 'Lead', 'Ochre', 'Limonite', 'FCR Weight', 'Sandstone', 'Limestone', 'Unmodified Stone', 'Misc. Stone', 'Charcoal', 'Wood', 'Seed', 'Nutshell', 'Textile', 'Misc. Botanical', 'Animal Bone', 'Shell', 'Bead', 'Button', 'Misc. Faunal', 'Whiteware', 'Stoneware', 'Earthenware', 'Procelain', 'Other Historic', 'Unidentified', 'Brick', 'Mortar', 'Misc. Historic', 'Sherd', 'Sherd Body', 'Sherd Rim', 'Vessel', 'Pipe', 'Stem', 'Fired Clay', 'Other Prehistoric', 'Unidentified', 'Misc. Prehistoric', 'Sample', 'Nail', 'Utensil', 'Horseshoe', 'Button', 'Gun Parts', 'Bullet', 'Casing', 'Misc. Metal', 'Container Fragments', 'Whole Container', 'Bead', 'Button', 'Misc. Glass', 'Plastic', 'Rubber', 'Other Misc.', 'Unidentified')

        self.init_widgets()

    def init_widgets(self):
        # Labels
        self.artifact_type_label = ttk.Label(self, text="Artifact Type", justify = tk.RIGHT)
        self.artifact_count_label = ttk.Label(self, text="Count", justify = tk.RIGHT)
        self.artifact_weight_label = ttk.Label(self, text="Weight (g)", justify = tk.RIGHT)

        # Entries
        self.artifact_type_entry = AutocompleteEntry(self)
        self.artifact_type_entry.set_completion_list(self.test_list)
        self.artifact_count_entry = ttk.Entry(self, width = 8)
        self.artifact_weight_entry = ttk.Entry(self, width = 8)

        # Buttons
        self.send_to_card = ttk.Button(self, text="Add to Card Preview", command = self.to_card, width=19)

        # Labels to Grid
        self.artifact_type_label.grid(row = 0, column = 0, padx = (10, 10), pady = (5, 10), sticky='e')
        self.artifact_count_label.grid(row = 0, column = 2, padx = (10, 0), pady = (5, 10), sticky='e')
        self.artifact_weight_label.grid(row = 0, column = 4, padx = (10, 0), pady = (5, 10), sticky='e')

        # Entries to grid
        self.artifact_type_entry.grid(row = 0, column = 1, padx = (10, 10), pady = (5, 10), sticky='e')
        self.artifact_count_entry.grid(row = 0, column = 3, padx = (10, 10), pady = (5, 10), sticky='e')
        self.artifact_weight_entry.grid(row = 0, column = 5, padx = (10, 10), pady = (5, 10), sticky='e')

        self.send_to_card.grid(row=0, column=6, padx = (37, 10), pady = (5, 10), sticky="nsew")

        # Entry list
        self.entry_ls = []
        self.entry_ls.append(self.artifact_type_entry)
        self.entry_ls.append(self.artifact_count_entry)
        self.entry_ls.append(self.artifact_weight_entry)

        # Bind entries
        self.bind_entries()

    def to_card(self):
        # Get data from entries
        data = self.get_data()

        # Check if data is valid
        invalid = False
        if data['ARTIFACT_TYPE'] == "" or data['ARTIFACT_TYPE'].isspace():
            invalid = True

        if data['ARTIFACT_COUNT'] == "" or data['ARTIFACT_COUNT'].isspace():
            pass
        else:
            try:
                int(data['ARTIFACT_COUNT'])
            except:
                invalid = True

        if data['ARTIFACT_WEIGHT'] == "" or data['ARTIFACT_WEIGHT'].isspace():
            invalid = True
        else:
            try:
                float(data['ARTIFACT_WEIGHT'])
            except:
                invalid = True
        
        if invalid == False:
            # Send data to card
            self.em.set("card_preview_frame", side = "back", dataset = data)

            # Wipe entries
            self.wipe()

            # Enable submit button
            self.em.set("submit_button", enabled = True)
        
    def get_data(self):
        artifact_dict = {'ARTIFACT_TYPE':str(self.entry_ls[0].get()),
                        'ARTIFACT_COUNT':str(self.entry_ls[1].get()),
                        'ARTIFACT_WEIGHT':str(self.entry_ls[2].get())}
        return artifact_dict

    def wipe(self):
        for i in self.entry_ls:
            i.delete(0, 'end')

    def bind_entries(self):
        self.artifact_count_entry.bind("<FocusOut>", self.validate_int) 
        self.artifact_count_entry.bind("<FocusIn>", self.validate_int)  
        self.artifact_count_entry.bind("<KeyRelease>", self.validate_int)

        self.artifact_weight_entry.bind("<FocusOut>", self.validate_float) 
        self.artifact_weight_entry.bind("<FocusIn>", self.validate_float)  
        self.artifact_weight_entry.bind("<KeyRelease>", self.validate_float)

    def validate_int(self, event):
        module = event.widget

        if module.get() == "" or module.get().isspace():
             module.state(["!invalid"])
        else:
            try:
                int(module.get())
                module.state(["!invalid"])
            except ValueError:
                module.state(["invalid"])

    def validate_float(self, event):
        module = event.widget

        if module.get() == "" or module.get().isspace():
            module.state(["!invalid"])
        else:
            try:
                float(module.get())
                module.state(["!invalid"])
            except ValueError:
                module.state(["invalid"])

class CardPreview(ttk.LabelFrame):
    def __init__(self, parent, app, text = "Card Preview"):
        super().__init__(parent, text = text)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.init_widgets()

    def init_widgets(self):
        self.front = tk.LabelFrame(self)
        self.front.pack(side="left", padx = 10, pady = (2, 8), fill = 'both', expand = 'true', anchor="nw")

        self.back = tk.LabelFrame(self)
        self.back.pack(side="right", padx = 10, pady = (2, 8), fill = 'both', expand = 'true', anchor="sw")

        # Text variables
        self.frontvar = tk.StringVar(self)
        self.backvar = tk.StringVar(self)

        # List of bag info for sql
        self.f_data = []

        # List of artifacts for preview
        self.b_string = []

        # List of artifacts for sql
        self.b_data = []

        site_num = 'Site:  ' + self.em.get('small_active_box_frame')[0] + '\n'

        self.frontvar.set(f"{site_num}Prov:                   \nCat#:                  \nMisc:                   \nName:                  \nDate:                   ")
        self.backvar.set("Artifact #1: (n) Ng     ")

        self.provenience_label = ttk.Label(self.front, textvariable=self.frontvar, font = ("Courier", 8, "italic"), justify = tk.LEFT)
        self.provenience_label.grid(row = 0, column = 0, padx=(10, 10), pady = (2, 5), sticky='e')

        self.artifact_label = ttk.Label(self.back, textvariable=self.backvar, font = ("Courier", 8, "italic"), justify = tk.LEFT)
        self.artifact_label.grid(row = 0, column = 0, padx=(10, 10), pady = (2, 5), sticky='e')

    def load_front(self, data):
        # Preformatted site number
        site_num = 'Site: ' + self.em.get('small_active_box_frame')[0] + '\n'

        self.f_data = data
        prefixes = ['Prov: ', 'Cat#: ', 'Misc: ', 'Name: ', 'Date: ']

        data_ls = []
        data_ls.append(data['prov'])
        data_ls.append(data['cat_num'])
        data_ls.append(data['other'])
        data_ls.append(data['name'])
        data_ls.append(data['date'])

        temp_data = []
        temp_prefixes=[]
        for i, j in zip(data_ls, prefixes):
            if not i.isspace() and i != '':
                temp_data.append(i)
                temp_prefixes.append(j)

        data_ls = temp_data
        prefixes = temp_prefixes

        if len(data_ls) >= 1:
            temp = []
            for i, j in zip(data_ls, prefixes):
                temp.append(self.format_front(i, j))

            joined = '\n'.join(temp)

            self.frontvar.set(site_num + joined)
        else:
            self.frontvar.set(f"{site_num}Prov:                   \nCat#:                  \nMisc:                   \nName:                  \nDate:                   ")

    def load_back(self, data):
        data['id']=len(self.b_data)

        self.b_data.append(data)
        if data['ARTIFACT_COUNT'] == "" or data['ARTIFACT_COUNT'].isspace():
            self.b_string.append(self.format_back(f"{data['ARTIFACT_TYPE']}: {data['ARTIFACT_WEIGHT']}g"))
        else:
            self.b_string.append(self.format_back(f"{data['ARTIFACT_TYPE']}: ({data['ARTIFACT_COUNT']}) {data['ARTIFACT_WEIGHT']}g"))
        
        self.backvar.set('\n'.join(self.b_string))

    def format_front(self, string, prefix):
        line_length = 18

        row = ''
        row_ls = []

        split = string.split()
        for i in range(len(split)-1):
            split[i] += '@'

        for word in split:
            if len(row) + len(word) - 1 > line_length:
                row_ls.append(row[0:-1])
                row = word
            else:
                row += word
        
        # Append final row
        spacing = ''
        for i in range(line_length - len(row)):
            spacing += '@'
        row_ls.append(row +  spacing)

        for i in range(len(row_ls)):
            if i == 0:
                row_ls[i] = prefix + row_ls[i]
            else:
                row_ls[i] = '      ' + row_ls[i]

        return '\n'.join(row_ls).replace('@', ' ')
    
    def update(self, id = 0):
        new_data = self.b_data.copy()

        # Pop id from list
        flag = False
        for i in range(len(new_data)):
            if flag == False:
                if int(new_data[i]['id']) == int(id):
                    new_data.pop(i)
                    flag = True
        
        self.b_data = []
        self.b_string = []
        self.backvar.set("Artifact #1: (n) Ng     ")

        for i in new_data:
            self.load_back(i)
            
    def format_back(self, string):
        # This number must be 6 more than the line_length of the format_front function
        line_length = 24

        row = ''
        row_ls = []

        split = string.split()
        for i in range(len(split)-1):
            split[i] += '@'

        for word in split:
            if len(row) + len(word) - 1 > line_length:
                row_ls.append(row[0:-1])
                row = word
            else:
                row += word
        
        # Append final row
        spacing = ''
        for i in range(line_length - len(row)):
            spacing += '@'
        row_ls.append(row +  spacing)

        return '\n'.join(row_ls).replace('@', ' ')

    def set(self, side = "front", dataset = {}):
        if side == "front":
            self.load_front(dataset)
        else:
            self.load_back(dataset)
    
    def set_back(self, id = 0):

        data = self.con.get_artifact_by_id(id)
        new_data = []

        for i in data:
            new_data.append({'ARTIFACT_TYPE':str(i[0]),
                             'ARTIFACT_COUNT':str(i[1]),
                             'ARTIFACT_WEIGHT':str(i[2])})
        self.b_data = []
        self.b_string = []
        self.backvar.set("Artifact #1: (n) Ng     ")

        for i in new_data:
            self.load_back(i)

    def get(self):
        return [self.f_data, self.b_data]

    def refresh(self):
        self.front.pack_forget()
        self.back.pack_forget()

        self.init_widgets()

class SubmitButton(ttk.LabelFrame):
    def __init__(self, parent, app, text = "", **kwargs):
        super().__init__(parent, text = text, **kwargs)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.is_update = False
        self.update_id = 0

        self.init_widgets()
    
    def init_widgets(self):
        # Buttons
        self.submit_button = ttk.Button(self, text = "Submit Bag to Database", command = self.submit, style="Accent.TButton")
        self.submit_button.pack(fill="both", expand="True", padx = 10, pady = (5, 12))

        # Disable submit button
        #self.disable()

    def submit(self):
        ls = self.em.get('card_preview_frame')
        artifact_ls = []

        if len(ls[1]) == 0:
            artifact_ls.append(Artifact(**{'ARTIFACT_TYPE': 'EMPTY', 'ARTIFACT_COUNT': 0, 'ARTIFACT_WEIGHT': 0}))
        elif len(ls[1]) == 1:
            artifact_ls.append(Artifact(**ls[1][0]))
        else:
            for i in ls[1]:
                artifact_ls.append(Artifact(**i))

        ls[0]['artifact_ls'] = artifact_ls

        bag = Bag(**ls[0])
        try:
            if self.is_update == True:
                self.con.delete_bag(self.update_id)
        except:
            print('Could not delete')

        self.con.insert_bag(bag)

        self.em.refresh('card_preview_frame')
        self.em.refresh('bag_treeview')

        self.em.refresh('additional_tools_window')

        # PDF
        data = self.con.get_pdf_view()
        if data != False:
            self.to_pdf()
            self.em.initialize('pdf_notification_window')

    def to_pdf(self):
        bag_data = self.con.get_pdf_view()
        bag_ls = []
        pd.set_option('display.max_colwidth', None)

        rand_ls = []
        ids = []
        flag = False
        for row in bag_data:
            if row[7] not in ids:
                ids.append(row[7])
                if flag == True:
                    bag_props['artifact_ls'] = artifact_ls.copy()
                    bag_ls.append(Bag(**bag_props.copy()))
                artifact_ls = []
                bag_props = {'Site': row[0],
                            'Prov': row[1], 
                            'Cat#': row[2], 
                            'Misc': row[3], 
                            'Name': row[4], 
                            'Date': row[5],
                            'artifact_ls': []}
                flag = True
            
            # Add artifact to list             
            artifact_ls.append(Artifact(**{'ARTIFACT_TYPE': row[15], 'ARTIFACT_COUNT': row[10], 'ARTIFACT_WEIGHT': row[11]}))
        
        # Append final bag
        bag_props['artifact_ls'] = artifact_ls.copy()
        bag_ls.append(Bag(**bag_props.copy()))

        filename = random.randint(100000000, 999999999)

        for id in ids:
            self.con.update_carded(id)

        file1 = PdfFile(bag_ls, 'Cards', str(filename))
        
    def set(self, enabled = "False"):
        if enabled:
            self.enable()
        else:
            self.disable()
    
    def update(self, id = 0):
        if id == -1:
            self.is_update = False
            self.update_id = 0
        else:
            self.is_update = True
            self.update_id = id

    def enable(self):
        self.submit_button['state'] = 'enabled'

    def disable(self):
        self.submit_button['state'] = 'disabled'