"""
tkentrycomplete.py

A tkinter widget that features autocompletion.

Created by Mitja Martini on 2008-11-29.
Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
Updated by Dominic Kexel to use tkinter and ttk instead of tkinter and tkinter.ttk
   Licensed same as original (not specified?), or public domain, whichever is less restrictive.
"""
import sys
import os
import tkinter
from tkinter import ttk
from time import sleep
from pynput.keyboard import Key, Controller


__version__ = "1.1"

# I may have broken the unicode...
tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(ttk.Entry):
        """
        Subclass of tkinter.Entry that features autocompletion.

        To enable autocompletion use set_completion_list(list) to define
        a list of possible strings to hit.
        To cycle through hits use down and up arrow keys.
        """
        def set_completion_list(self, completion_list):
                self.keyboard = Controller()
                self.in_prog = 0
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)

        def autocomplete(self, delta=0):
                """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()):  # Match case-insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        #pos = len(self.get()) - len(self._hits[self._hit_index])
                        if len(self._hits[self._hit_index]) <= len(self.get()):
                            self.delete(len(self._hits[self._hit_index]),tkinter.END)
                        else:
                            self.delete(0,tkinter.END)
                            self.insert(0,self._hits[self._hit_index])
                            self.select_range(self.position,tkinter.END)
                self.in_prog = 0
                        

        def handle_keyrelease(self, event):
                    """event handler for the keyrelease event on this widget"""
                    if event.keysym == "BackSpace":
                            self.delete(self.index(tkinter.INSERT), tkinter.END)
                            self.position = self.index(tkinter.END)
                    if event.keysym == "Left":
                            if self.position < self.index(tkinter.END): # delete the selection
                                    self.delete(self.position, tkinter.END)
                            else:
                                    self.position = self.position-1 # delete one character
                                    self.delete(self.position, tkinter.END)
                    if event.keysym == "Right":
                            self.position = self.index(tkinter.END) # go to end (no selection)
                    if event.keysym == "Down":
                            self.autocomplete(1) # cycle to next hit
                    if event.keysym == "Up":
                            self.autocomplete(-1) # cycle to previous hit
                    if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
                            self.autocomplete()
                        

class AutocompleteCombobox(ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END)
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(tkinter.END) # go to end (no selection)
                #if len(event.keysym) == 1:
                #        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion

def test(frame):
        root = tkinter.Tk(className=' AutocompleteEntry demo')
        root.title("Artifact Entry")
        root.tk.call("source", "sun-valley.tcl")
        root.tk.call("set_theme", "light")
        entry = AutocompleteEntry(frame)
        entry.set_completion_list(test_list)
        entry.pack()
        entry.focus_set()
        combo = AutocompleteCombobox(root)
        combo.set_completion_list(test_list)
        combo.pack()
        combo.focus_set()
        # I used a tiling WM with no controls, added a shortcut to quit
        root.bind('<Control-Q>', lambda event=None: root.destroy())
        root.bind('<Control-q>', lambda event=None: root.destroy())
        root.mainloop()

if __name__ == '__main__':


        test_list = ('Debitage', 'Utilized Debitage', 'Biface', 'Hafted Biface - Side Notch', 'Hafted Biface - Corner Notch', 'Hafted Biface - Basal Notch', 'Hafted Biface - Stemmed', 'Hafted Biface - Lanceolate', 'Axe', 'Adze', 'Core', 'Drill', 'Uniface', 'Misc. Chipped Stone', 'Groundstone', 'Abrader', 'Mano', 'Metate', 'Nuttingstone', 'Hammerstone', 'Hematite', 'Lead', 'Ochre', 'Limonite', 'FCR Weight', 'Sandstone', 'Limestone', 'Unmodified Stone', 'Misc. Stone', 'Charcoal', 'Wood', 'Seed', 'Nutshell', 'Textile', 'Misc. Botanical', 'Animal Bone', 'Shell', 'Bead', 'Button', 'Misc. Faunal', 'Whiteware', 'Stoneware', 'Earthenware', 'Procelain', 'Other Historic', 'Unidentified', 'Brick', 'Mortar', 'Misc. Historic', 'Sherd', 'Sherd Body', 'Sherd Rim', 'Vessel', 'Pipe', 'Stem', 'Fired Clay', 'Other Prehistoric', 'Unidentified', 'Misc. Prehistoric', 'Sample', 'Nail', 'Utensil', 'Horseshoe', 'Button', 'Gun Parts', 'Bullet', 'Casing', 'Misc. Metal', 'Container Fragments', 'Whole Container', 'Bead', 'Button', 'Misc. Glass', 'Plastic', 'Rubber', 'Other Misc.', 'Unidentified')
        test(test_list)