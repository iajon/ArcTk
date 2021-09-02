import tkinter as tk
from tkinter import ttk
from lib.Classes import Box

class BoxEntryWindow(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        # Title
        self.title("New Box (+)")

        # Theme
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "light")

        self.init_widgets()
    
    def init_widgets(self):
        # Frame
        self.frame = ttk.LabelFrame(self)
        self.frame.pack(padx = 10, pady = (5, 10))

        # Labels
        self.site_num = ttk.Label(self.frame, text="Site Number", justify = tk.RIGHT)
        self.site_name = ttk.Label(self.frame, text="Site Name", justify = tk.RIGHT)
        self.oin = ttk.Label(self.frame, text="Old Inventory\nNumber(s)", justify = tk.RIGHT)
        self.snum = ttk.Label(self.frame, text="Shelving Number", justify = tk.RIGHT)
        self.inum = ttk.Label(self.frame, text="Ident. Number", justify = tk.RIGHT)
        
        self.collectors = ttk.Label(self.frame, text="Collectors", justify = tk.RIGHT)
        self.years = ttk.Label(self.frame, text="Years", justify = tk.RIGHT)
        self.pname = ttk.Label(self.frame, text="Project Name", justify = tk.RIGHT)
        self.ptype = ttk.Label(self.frame, text="Project Type", justify = tk.RIGHT)
        self.contract = ttk.Label(self.frame, text="Contract No.", justify = tk.RIGHT)

        # Labels to grid
        self.site_num.grid(row = 0, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')
        self.site_name.grid(row = 1, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')
        self.oin.grid(row = 2, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')
        self.snum.grid(row = 3, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')
        self.inum.grid(row = 4, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')

        self.collectors.grid(row = 0, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')
        self.years.grid(row = 1, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')
        self.pname.grid(row = 2, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')
        self.ptype.grid(row = 3, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')
        self.contract.grid(row = 4, column = 2, padx=(10, 10), pady = (10, 10), sticky='e')

        # Entries
        self.site_num_entry = ttk.Entry(self.frame)
        self.site_name_entry = ttk.Entry(self.frame)
        self.oin_entry = ttk.Entry(self.frame)
        self.snum_entry = ttk.Entry(self.frame)
        self.inum_entry = ttk.Entry(self.frame)

        self.collectors_entry = ttk.Entry(self.frame)
        self.years_entry = ttk.Entry(self.frame)
        self.pname_entry = ttk.Entry(self.frame)
        self.ptype_entry = ttk.Entry(self.frame)
        self.contract_entry = ttk.Entry(self.frame)

        # Entries to grid
        self.site_num_entry.grid(row = 0, column = 1,  padx=(10, 10), pady = (10, 5))
        self.site_name_entry.grid(row = 1, column = 1,  padx=(10, 10), pady = (5, 5))
        self.oin_entry.grid(row = 2, column = 1,  padx=(10, 10), pady = (5, 5))
        self.snum_entry.grid(row = 3, column = 1,  padx=(10, 10), pady = (5, 5))
        self.inum_entry.grid(row = 4, column = 1,  padx=(10, 10), pady = (5, 10))

        self.collectors_entry.grid(row = 0, column = 3,  padx=(10, 10), pady = (10, 5))
        self.years_entry.grid(row = 1, column = 3,  padx=(10, 10), pady = (5, 5))
        self.pname_entry.grid(row = 2, column = 3,  padx=(10, 10), pady = (5, 5))
        self.ptype_entry.grid(row = 3, column = 3,  padx=(10, 10), pady = (5, 5))
        self.contract_entry.grid(row = 4, column = 3,  padx=(10, 10), pady = (5, 10))

        # Separators
        self.separator = ttk.Separator(self.frame)
        self.separator.grid(row = 5, column = 0, columnspan = 4, padx = 10, sticky = 'ew')

        self.entry_ls = []
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

        # Buttons
        self.submit_button = ttk.Button(self.frame, text="Submit Box", command = self.submit_box, style="Accent.TButton")
        self.cancel_button = ttk.Button(self.frame, text="Cancel", command = self.destroy)

        self.submit_button.grid(row=6, column=0, columnspan = 4, padx = 150, pady = (10, 10), sticky="nsew")
        self.cancel_button.grid(row=6, column=3, padx = (0, 10), pady = (10, 10), sticky="nse")

    def submit_box(self):
        box_ls = []
        for i in self.entry_ls:
            temp = i.get()
            if temp.isspace() or temp == "":
                box_ls.append("N/A")
            else:
                box_ls.append(temp)

        dict = {'site_num' : box_ls[0],
                'site_name' : box_ls[1],
                'oin' : box_ls[2],
                'shelving_num' : box_ls[3],
                'id_num' : box_ls[4],
                'collectors' : box_ls[5],
                'years' : box_ls[6],
                'pname' : box_ls[7],
                'ptype' : box_ls[8],
                'contract' : box_ls[9]}

        if dict['site_num'] == "N/A":
            dict['site_num'] = "23OTHER"
        box = Box(**dict)

        self.con.insert_box(box, 1)
        self.em.refresh('active_box_frame')
        self.em.refresh('small_active_box_frame')
        self.destroy()

    def disable(self):
        for i in self.entry_ls:
            i['state'] = 'disabled'