import tkinter as tk
from tkinter import ttk
from tkinter.constants import NO, TRUE

class BagView(ttk.Treeview):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent,  **kwargs)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.index = 0
        self.insert_ls = []

        self.init_tree()

    def init_tree(self):
        # Define columns
        self['columns'] = ("SiteNum", "Prov", "CatNum", "Other", "Name", "Date", "Type", "Count", "Weight")

        # Format columns
        self.column("#0", width=20, minwidth = 20)
        self.column("SiteNum", anchor = "w", width=80)
        self.column("Prov", anchor = "w", width=240)
        self.column("CatNum", anchor = "w", width=100)
        self.column("Other", anchor = "w", width=120)
        self.column("Name", anchor = "w", width=120)
        self.column("Date", anchor = "w", width=120)
        self.column("Type", anchor = "w", width=150, minwidth = 150)
        self.column("Count", anchor = "center", width=60, minwidth = 60)
        self.column("Weight", anchor = "center", width=80)

        # Create headings
        self.heading("#0", text = "", anchor = "center")
        self.heading("SiteNum", text = "Site Number", anchor = "center")
        self.heading("Prov", text = "Provenience", anchor = "center")
        self.heading("CatNum", text = "Cat. #", anchor = "center")
        self.heading("Other", text = "Other Labels", anchor = "center")
        self.heading("Name", text = "Name(s)", anchor = "center")
        self.heading("Date", text = "Date(s)", anchor = "center")
        self.heading("Type", text = "Artifact Type", anchor = "center")
        self.heading("Count", text = "Count", anchor = "center")
        self.heading("Weight", text = "Weight", anchor = "center")

        self.load()

    # Load most recent bag
    def load(self):
        selection = self.con.get_bag_by_box()
        sel_ls = []
        last_id = selection[0][0]
        
        for row in selection:
            row = list(row)
            if row[0] == last_id:
                if len(sel_ls):
                    sel_ls[-1].append(row)
                else:
                    sel_ls.append([row])
            else:
                sel_ls.append([row])
                last_id = row[0]
        
        for i in sel_ls:
            self.to_tree(i)
        self.see(self.insert_ls[-1])
        
    # Pull most recent bag and insert
    def update(self):
        selection = self.con.get_bag_by_active()
        sel_ls = []

        for row in selection:
            sel_ls.append(list(row))

        self.to_tree(sel_ls)
        self.see(self.insert_ls[-1])

    # Insert selection to tree       
    def to_tree(self, selection):
        firstrow = True
        parent = self.iid()
        for row in selection:
            if len(str(row[-1])):
                row[-1] = str(row[-1]) + 'g'
            if firstrow == True:
                self.insert_ls.append(self.insert('', index = 'end', iid = parent, values = row[1:]))
                firstrow = False
            else:
                row = ("", "", "", "", "", "", "", row[7], row[8], row[9])
                self.insert(parent, index = 'end', iid = self.iid(), values = row[1:])

    # Get/increments index
    def iid(self, val = True):
        if val == True:
            self.index += 1
        return self.index

    def refresh(self):
        self.update()

    # Wipe treeview
    def wipe(self):
        self.delete(*self.get_children())

class BoxView(ttk.Treeview):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.em = app.event_manager
        self.con = app.connection

        self.index = 0
        self.insert_ls = []

        self.init_tree()

    def init_tree(self):
        # Define columns
        self['columns'] = ("box_id", "sitenum", "sitename", "oin", "snum", "collectors", "years", "pname", "ptype", "processed")

        # Format columns
        self.column("#0", width=0, stretch = NO)
        self.column("box_id", anchor = "w", width=100)
        self.column("sitenum", anchor = "w", width=100)
        self.column("sitename", anchor = "w", width=120)
        self.column("oin", anchor = "w", width=120)
        self.column("snum", anchor = "w", width=120)
        self.column("collectors", anchor = "w", width=120)
        self.column("years", anchor = "w", width=130, minwidth = 130)
        self.column("pname", anchor = "center", width=90, minwidth = 90)
        self.column("ptype", anchor = "center", width=110)
        self.column("processed", anchor = "center", width=80)

        # Create headings
        self.heading("#0", text = "", anchor = "center")
        self.heading("box_id", text = "Box ID", anchor = "center")
        self.heading("sitenum", text = "Site Number", anchor = "center")
        self.heading("sitename", text = "Site Name", anchor = "center")
        self.heading("oin", text = "Old Inv. Num(s)", anchor = "center")
        self.heading("snum", text = "Shelving Num(s)", anchor = "center")
        self.heading("collectors", text = "Collectors", anchor = "center")
        self.heading("years", text = "Years", anchor = "center")
        self.heading("pname", text = "Project Name", anchor = "center")
        self.heading("ptype", text = "Project Type", anchor = "center")
        self.heading("processed", text = "Processed?", anchor = "center")

        self.load()

    # Load most recent box
    def load(self):
        selection = self.con.get_box_by_unprocessed()
        sel_ls = []
        last_id = selection[0][0]
        
        for row in selection:
            row = list(row)
            if row[0] == last_id:
                if len(sel_ls):
                    sel_ls[-1].append(row)
                else:
                    sel_ls.append([row])
            else:
                sel_ls.append([row])
                last_id = row[0]
        
        for i in sel_ls:
            self.to_tree(i)
        self.see(self.insert_ls[-1])
        
    # Pull most recent box and insert
    def update(self):
        selection = self.con.get_bag_by_active()
        sel_ls = []

        for row in selection:
            sel_ls.append(list(row))

        self.to_tree(sel_ls)
        self.see(self.insert_ls[-1])

    # Insert selection to tree       
    def to_tree(self, selection):
        firstrow = True
        for row in selection:
            if str(row[-1]) != '1':
                row[-1] = "False"
            
            self.insert_ls.append(self.insert('', index = 'end', iid = self.iid(), values = row))

    # Get/increments index
    def iid(self, val = True):
        if val == True:
            self.index += 1
        return self.index

    # Wipe treeview
    def wipe(self):
        self.delete(*self.get_children())
