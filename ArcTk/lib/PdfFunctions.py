import fpdf
import pandas as pd

from lib.Pdf_Object_Tests import Typewriter
import lib.GeneralFunctions as gf
from lib.Classes import Bag, Card, Artifact

class PdfFile:
    def __init__(self, bag_ls, site, inv):
        # Initialize PDF
        self.pdfs = fpdf.FPDF(format='letter')
        self.pdfs.set_font("Courier", size=6)

        # Num cards per row, page width in (points?)
        self.cards_per_row = 5
        self.card_width = 196/self.cards_per_row

        #Sort list of bags by newln_ct
        bag_ls = sorted(bag_ls, key=lambda x: -x.card.newln_ct)

        # Get list of row newln counts
        newln_ls = to_ls(bag_ls, self.cards_per_row)

        # Add blank cards so columns are even
        bag_ls = insert_blank_cards(bag_ls, newln_ls[-1], self.cards_per_row)

        # Make num newln same for all cards
        bag_ls = level_rows(bag_ls, newln_ls, self.cards_per_row)

        # Split card objects into front_ls and back_ls
        df = split_info(bag_ls, self.cards_per_row)

        # Write front and back to PDF
        t = Typewriter(site, inv)
        t.type_all(df[0], df[1], newln_ls, 0)

    # Write list to PDF
    def write_to_pdf(self, ls, newln_ls):
        # Add new page
        self.pdf.add_page()

        # Tracks current card row and column
        card_x = 0
        card_y = 0

        # Tracks current line (99 total lines on page)
        current_line = 0

        # Establish offsets 
        y_offset = self.pdf.y
        x_offset = self.pdf.x + self.card_width

        for i in ls:
            # If beginning of new row
            if card_x == 0:
                if current_line + newln_ls[card_y] >= 98:
                    pdf.add_page()
                    current_line = 0

            # Set offsets according to current cords
            y_offset = self.pdf.y
            x_offset = self.pdf.x + self.card_width

            # Print card
            self.pdf.multi_cell(self.card_width, 2.5, i, 1, 0)

            # Set pdf coords to offsets
            self.pdf.y = y_offset
            self.pdf.x = x_offset

            # Increment card_x (column)
            card_x += 1

            # If end of row
            if card_x == self.cards_per_row:

                # For num newln at current card row (card_y)
                for x in range(newln_ls[card_y] + 1):
                    self.pdf.ln()
                
                current_line += newln_ls[card_y] + 1
                card_y += 1
                card_x = 0

# Gets newln_ct for first bag in each row, returns as list
def to_ls(ls, cards_per_row):
    ct_ls = []
    x = 0

    for i in ls:
        if x == 0:
            ct_ls.append(i.card.newln_ct)
        elif x == cards_per_row - 1:
            x = -1
        x += 1
    
    return ct_ls

def pre_suf_split(ls):
    ls = ls.copy()

    temp_ls = []

    pre = []
    suff = []

    for i in ls:
        while ':' in i:
            idx = i[i.index(':')]
            temp_ls.append(i[:idx] + '\n')
            i = i[idx:]
        temp_str = ''.join(temp_ls)
        temp_ls = []
        pre.append(temp_str)
    
# Inserts empty bags for double-sided printing (needed to ensure back side lines up
# with front after mirrored over y-axis)
def insert_blank_cards(bag_ls, newln_ls, cards_per_row):
    s = ''
    temp_ls = []
    remainder = len(bag_ls) % cards_per_row

    if remainder == 0:
        iterations = 0
    else:
        iterations = cards_per_row - remainder

    for i in range(iterations):
        temp_ls.append(Bag(**{}, artifact_ls = [Artifact(**{'BLANK':''})]))
    for i in temp_ls:
        i.card.newln_ct = newln_ls
    return bag_ls + temp_ls

# Returns a dataframe with columns 'Front' and 'Back' where 'Back' is mirrored across the 
# y-axis for double-sided printing
def split_info(bag_ls, cards_per_row):
    front_ls = []
    back_ls = []

    x = cards_per_row 
    row = 1
    reverse = x * row

    for i in range(len(bag_ls)):
        reverse -= 1
        x -= 1

        front_ls.append(bag_ls[i].card.card_front)
        back_ls.append(bag_ls[reverse].card.card_back)

        if x == 0:
            row += 1
            x = cards_per_row
            reverse = x * row 

    return [front_ls, back_ls] 

# Adds newln (\n) for difference between first card in row and current card
def level_rows(bag_ls, newln_ls, cards_per_row):
    x = 0
    row = 0

    for i in bag_ls:
        if gf.check_key(i.__dict__, 'BLANK'):
            pass
        else:
            for j in range(newln_ls[row] - i.card.newln_ct):
                i.card.card_front += '\n '
                i.card.card_back += '\n '
                i.card.newln_ct += 1
        
        if x == cards_per_row - 1:
            x = -1
            row += 1

        x += 1

    return bag_ls
