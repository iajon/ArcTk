#!/usr/bin/env python
# -*- coding: utf8 -*-

import fpdf

from lib.GeneralFunctions import replace_chars

class Typewriter:
    def __init__(self, site, inv):
        self.pdf = fpdf.FPDF(format='letter')
        self.pdf.set_font("Courier", style = 'i', size=6)
        
        if len(inv) > 0:
            self.filename = f"file_output\{site}_{inv}.pdf"
        else:
            self.filename = f"file_output\{site}_001.pdf"

        self.cards_per_row = 5
        self.card_width = 196/self.cards_per_row

        self.x_offset = 0
        self.y_offset = 0
        
        self.card_x = 0
        self.card_y = 0

        self.current_line = 0
        self.max_line = 99

        self.front_side = True

        self.border = True

        self.f_iter = 0
        self.b_iter = 0

        self.feed_page()
    
    def set_style(self, style_code):
        # Prefixes
        if style_code == 0:
            self.border = True
            self.pdf.set_font("Courier", style = 'I', size=6)
        
        # Back
        elif style_code == 2:
            self.border = False
            self.pdf.set_font("Courier", style = 'I', size=6)

        # Information
        elif style_code == 1:
            self.border = False
            self.pdf.set_font("Courier", style = 'I', size=6)
        
        # Default
        else:
            self.border = True
            self.pdf.set_font("Courier", style = '', size=6)
            
    def feed_page(self):
        self.pdf.add_page()
        self.card_x = 0
        self.card_y = 0
        self.current_line = 0
    
    def return_carraige(self, num_lines):
        for i in range(num_lines):
            self.pdf.ln()
        self.card_x = 0
        self.card_y += 1
        self.current_line += num_lines

    def type_row(self, ls, num_lines, offset_type):
        if self.current_line + num_lines >= self.max_line:
            self.feed_page()
            self.front_side = not self.front_side
            return None

        inc = 0
        for i in ls:
            i = replace_chars(i)
            self.y_offset = self.pdf.y
            self.x_offset = self.pdf.x + self.card_width

            self.set_style(offset_type)
            
            self.pdf.multi_cell(self.card_width, 2.5, str(i), self.border, 0)

            self.pdf.y = self.y_offset
            self.pdf.x = self.x_offset

            self.card_x += 1
        
        self.return_carraige(num_lines)
        
    def call_t(self, ls, num_lines):
        self.type_row(ls, num_lines)
        self.feed_page()
        self.type_row(ls, num_lines)
        self.pdf.output(self.filename)
    
    def type_all(self, ls_f, ls_b, num_lines_f, offset_type):
        num_lines_b = list(num_lines_f)
        length = len(ls_f) + len(ls_b)
        cpr = self.cards_per_row

        inc = 1

        for i in range(length):

            if len(ls_f) + len(ls_b) == 0:
                self.pdf.output(self.filename)
                return None

            if self.front_side == True:
                self.type_row(ls_f[:cpr], num_lines_f[0], offset_type)
                inc += 1
                del ls_f[:cpr]
                del num_lines_f[0]

                if len(ls_f) == 0:
                    self.feed_page()
                    self.front_side = False
                
            elif self.front_side == False:
                self.type_row(ls_b[:cpr], num_lines_b[0], 2)
                del ls_b[:cpr]
                del num_lines_b[0]

                if len(ls_b) == 0:
                    self.pdf.output(self.filename)
                    self.front_side = True
                    return None

        self.pdf.output(self.filename, 'F')
        
        


    


        