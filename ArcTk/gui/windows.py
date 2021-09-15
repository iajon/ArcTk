from lib.PdfFunctions import PdfFile
import tkinter as tk
from tkinter import ttk

from itertools import chain

from lib.Classes import Box, Bag, Artifact
import lib.GeneralFunctions as gf
import lib.HtmlFunctions as hf

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
        self.em.refresh('box_treeview')
        self.destroy()

    def disable(self):
        for i in self.entry_ls:
            i['state'] = 'disabled'

class SetActiveBoxWindow(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        # Title
        self.title("Select Box")

        # Theme
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "light")

        # Valid box IDs
        self.box_id_ls = list(chain(*self.con.get_box_ids()))

        self.init_widgets()
    
    def init_widgets(self):
        # Frame
        self.frame = ttk.LabelFrame(self)
        self.frame.pack(padx = 10, pady = (5, 10))

        # Labels
        self.box_id = ttk.Label(self.frame, text="Box ID", justify = tk.RIGHT)
        self.error_msg = ttk.Label(self.frame, text="Error: Box ID does not exist!", justify = tk.CENTER)
        self.invalid_msg = ttk.Label(self.frame, text="Error: Box ID is invalid!", justify = tk.CENTER)

        # Labels to grid
        self.box_id.grid(row = 0, column = 0, padx=(10, 10), pady = (10, 10), sticky='e')

        # Entries
        self.box_id_entry = ttk.Entry(self.frame)

        # Entries to grid
        self.box_id_entry.grid(row = 0, column = 1,  padx=(10, 10), pady = (10, 10))

        # Separators
        self.separator = ttk.Separator(self.frame)
        self.separator.grid(row = 1, column = 0, columnspan = 4, padx = 10, sticky = 'ew')

        # Buttons
        self.select_button = ttk.Button(self.frame, text="Set Box as Active", command = self.select_box, style="Accent.TButton")

        # Buttons to grid
        self.select_button.grid(row=2, column=0, columnspan = 2, padx = 10, pady = (10, 10), sticky="nsew")

        # Bind entries
        self.bind_entries()

    def select_box(self):
        self.error_msg.grid_forget()
        self.invalid_msg.grid_forget()

        try:
            id = int(self.box_id_entry.get())

            if id in self.box_id_ls:
                self.con.set_active_box(id)
                self.em.refresh('active_box_frame')
                self.em.refresh('small_active_box_frame')
                self.em.refresh('box_treeview')
                self.em.refresh('bag_treeview')
                self.em.refresh('card_preview_frame')
                self.destroy()
            else:
                self.error_msg.grid(row = 3, column = 0, columnspan=2, padx=(10, 10), pady = (10, 10))
        except ValueError:
            self.invalid_msg.grid(row = 3, column = 0, columnspan=2, padx=(10, 10), pady = (10, 10))

    def bind_entries(self):
        self.box_id_entry.bind("<FocusOut>", self.validate_id) 
        self.box_id_entry.bind("<FocusIn>", self.validate_id)  
        self.box_id_entry.bind("<KeyRelease>", self.validate_id)

    def validate_id(self, event):
        module = event.widget

        if module.get() == "" or module.get().isspace() or module.get() not in self.box_id_ls:
            module.state(["!invalid"])
        else:
            try:
                int(module.get())
                module.state(["!invalid"])
            except ValueError:
                module.state(["invalid"])

class ExportBoxWindow(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.em = app.event_manager
        self.con = app.connection
        self.app = app

        # Title
        self.title("Export Box")

        # Theme
        self.tk.call("source", "sun-valley.tcl")
        self.tk.call("set_theme", "light")

        self.init_widgets()
    
    def init_widgets(self):
        # Frame
        self.frame = ttk.LabelFrame(self)
        self.frame.pack(padx = 10, pady = (5, 10))

        # Labels
        warning_text = "*Please verify that the appropriate box is selected."
        self.warnings = ttk.Label(self.frame, text=warning_text)

        self.site_num = ttk.Label(self.frame, text="Site Name")
        self.oin = ttk.Label(self.frame, text="Old Inventory Number(s)")

        self.bag_count = ttk.Label(self.frame, text=f"Bag Total: {self.con.get_count()} Bags")
        self.page_count = ttk.Label(self.frame, text="Page Total: 5 Pages")

        # Entries
        self.site_num_entry = ttk.Entry(self.frame)
        self.oin_entry = ttk.Entry(self.frame)

        selection = self.con.get_box(target = "active")[0]
        self.site_num_entry.delete(0, tk.END)
        self.site_num_entry.insert(0, selection[0])

        self.oin_entry.delete(0, tk.END)
        self.oin_entry.insert(0, selection[4])

        self.site_num_entry['state'] = 'disabled'
        self.oin_entry['state'] = 'disabled'

        # Labels to grid
        self.warnings.grid(row = 0, column = 0, columnspan = 2, padx=(10, 10), pady = (10, 10), sticky='w')

        # Separators
        self.separator = ttk.Separator(self.frame)
        self.separator.grid(row = 1, column = 0, columnspan = 4, padx = 10, sticky = 'ew')

        # Labels to grid
        self.site_num.grid(row = 2, column = 0, padx=(10, 10), pady = (10, 0), sticky='w')
        self.oin.grid(row = 2, column = 1, padx=(10, 10), pady = (10, 0), sticky='w')

        self.bag_count.grid(row = 4, column = 0, padx=(10, 10), pady = (0, 10))
        self.page_count.grid(row = 4, column = 1, padx=(10, 10), pady = (0, 10))

        # Entries to grid
        self.site_num_entry.grid(row = 3, column = 0,  padx=(10, 10), pady = (5, 10))
        self.oin_entry.grid(row = 3, column = 1,  padx=(10, 10), pady = (5, 10))

        # Export Settings Frame
        self.es_frame = ttk.LabelFrame(self, text="Export Settings")
        self.es_frame.pack(padx = 10, pady = (5, 10))

        # Checkbuttons
        self.excel_var = tk.IntVar(self)
        self.excel_var.set(0)
        self.excel_cb = ttk.Checkbutton(self.es_frame, text="Export Excel", variable = self.excel_var)
        self.excel_cb.grid(row = 0, column = 0, padx = (10, 10), pady = (10, 10), sticky="ew")

        self.html_var = tk.IntVar(self)
        self.html_var.set(0)
        self.html_cb = ttk.Checkbutton(self.es_frame, text="Export HTML", variable = self.html_var)
        self.html_cb.grid(row = 0, column = 1, padx = (10, 10), pady = (10, 10), sticky="ew")

        self.pdf_var = tk.IntVar(self)
        self.pdf_var.set(0)
        self.pdf_cb = ttk.Checkbutton(self.es_frame, text="Export PDF", variable = self.pdf_var)
        self.pdf_cb.grid(row = 0, column = 2, padx = (10, 10), pady = (10, 10), sticky="ew")

        # Buttons
        self.export_button = ttk.Button(self.es_frame, text="Export Box", command = self.export_box, style="Accent.TButton")
        self.export_button.grid(row=1, column=0, columnspan = 3, padx = 10, pady = (10, 10), sticky="nsew")

    def export_box(self):
        selection = self.con.get_box_for_export()

        # Begin filtering
        # Remove box information from bags
        box_data = list(selection[0][0:10])
        bag_data = []
        for row in selection:
            bag_data.append(list(row[10:]))

        # Create a list of bags
        bag_ls = []
        artifact_ls = []

        bag_props = {'prov': '', 
                    'cat_num': '', 
                    'other': '', 
                    'name': '', 
                    'date': '',
                    'artifact_ls': []}

        current_id = 0
        flag = False
        for row in bag_data:
            # If new bag id
            if current_id != row[-1]:
                if flag == False:
                    flag = True    
                else:
                    # Append bag
                    bag_props['artifact_ls'] = artifact_ls
                    bag_ls.append(Bag(**bag_props.copy()))

                # Clear bag data/set id
                current_id = row[-1]
                artifact_ls = []
                bag_props = {'Site': box_data[0],
                            'Prov': row[0], 
                            'Cat#': row[1], 
                            'Misc': row[2], 
                            'Name': row[3], 
                            'Date': row[4],
                            'artifact_ls': []}

            # Add artifact to list             
            artifact_ls.append(Artifact(**{'ARTIFACT_TYPE': row[5], 'ARTIFACT_COUNT': row[6], 'ARTIFACT_WEIGHT': row[7]}))
        
        # Append final bag
        bag_props['artifact_ls'] = artifact_ls
        bag_ls.append(Bag(**bag_props.copy()))

        # Prep for output
        sitenum = box_data[0]
        invnum = box_data[2]

        # Uncomment to print list of bags
        """
        for i in bag_ls:
            print(f"Bag info: {i.__dict__}")
            for x in i.artifact_ls:
                print(x.__dict__)
        """

        if (self.excel_var.get()):
            self.export_to_excel(bag_ls, sitenum, invnum)
        if (self.html_var.get()):
            self.export_to_html(bag_ls, sitenum, invnum)
        if (self.pdf_var.get()):
            self.export_to_pdf(bag_ls, sitenum, invnum)
    
    def export_to_excel(self, bag_ls, site, inv):
        pass

    def export_to_html(self, bag_ls, site, inv):
        cat_ls = gf.get_cat_nums(bag_ls)
        for i in range(len(cat_ls)):
            cat_ls[i] += ';'

        prov_ls = gf.get_prov_ls(bag_ls)
        for i in range(len(prov_ls)):
            prov_ls[i] += ';'

        if (len(inv) > 0):
            filename = f"{site}_{inv}"
        else:
            filename = f"{site}_001"

        hf.write_html(filename, site, inv, prov_ls, cat_ls)

    def export_to_pdf(self, bag_ls, site, inv):

        file_1 = PdfFile(bag_ls, site, inv)

                



