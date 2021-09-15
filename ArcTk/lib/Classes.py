import sqlite3 as sl

from enum import Enum, auto
from datetime import date

#import queries as qr
import lib.GeneralFunctions as gf
import sql.queries as qr
#import ExcelFunctions as xlf


class ArtifactType(Enum):
    """Artifact Types"""

    #Debitage
    DEBITAGE = auto()
    UTIL_DEB = auto()

    #Chipped Stone
    BIFACE = auto()
    HAFT_BIF = auto()
    HAFT_BIF_SN = auto()
    HAFT_BIF_CN = auto()
    HAFT_BIF_BN = auto()
    HAFT_BIF_S = auto()
    HAFT_BIF_L = auto()
    AXE = auto()
    ADZE = auto()
    CORE = auto()
    DRILL = auto()
    UNIFACE = auto()

class Artifact:
    """Artifacts of the same type within a bag"""

    def __init__(self, **properties):
        
        # Set attr: count, weight
        for keyword, value in properties.items():
            setattr(self, keyword, value)
        
        # Set attr: artifact_type, string
        self.string = gf.replace_chars(self.make_string())
        
    
    # Creates string for printing on cards, format: 'ArtifactType: (count) weightg'
    def make_string(self):

        artifact_dict = self.__dict__
        temp_ls = []

        if gf.check_key(artifact_dict, 'BLANK'):
            return artifact_dict['BLANK']

        if gf.check_key(artifact_dict, 'ARTIFACT_TYPE'):
            temp_ls.append("%s:" % str(artifact_dict.get('ARTIFACT_TYPE')))

        if gf.check_key(artifact_dict, 'ARTIFACT_COUNT'):
            if artifact_dict.get('ARTIFACT_COUNT') != '':
                temp_ls.append("(%s)" % artifact_dict.get('ARTIFACT_COUNT'))

        if gf.check_key(artifact_dict, 'ARTIFACT_WEIGHT'):
            temp_ls.append("%sg" % artifact_dict.get('ARTIFACT_WEIGHT'))

        return ' '.join(temp_ls)

class Bag:
    """Bag containing one or more artifact types"""

    def __init__(self, **properties):

        for keyword, value in properties.items():
            setattr(self, keyword, value)
    
        if 'Date' in self.__dict__.keys():
            self.format_date()
        self.card = Card(self)
    
    def format_date(self):
        ls = str(self.Date).split()
        if len(ls) > 0:
            self.Date = str(ls[0])

    def to_db(self):
        qr.insert_bag(self)
        for i in self.artifact_ls:
            qr.insert_artifact(i)
            
class Box:
    """Box containing bags"""

    def __init__(self, **properties):
        for keyword, value in properties.items():
            setattr(self, keyword, value)

        if self.site_num != None:
            self.state = self.site_num[0:2]
            self.county = self.site_num[2:4]
        else:
            self.site_num = "23OTHER"
    

class Card:
    """Stores information about the bag"""

    def __init__(self, bag):
        self.newln_ct = 0
        self.bag = bag
        self.artifacts = self.bag.artifact_ls

        self.load_front()
        self.load_back()
        self.level()
        
        self.newln_ct = self.front_ct

    def load_front(self):
        prefixes = []
        data = []

        bag_dict = self.bag.__dict__
        bag_dict.pop('artifact_ls', None)

        for k, v in bag_dict.items():
            if not isinstance(v, list):
                if v == '' or v.isspace():
                    pass
                else:
                    prefixes.append(k + ': ')
                    data.append(str(v))
        
        rows = []
        ct = 0
        for i, j in zip(prefixes, data):
            values = self.format_front(i, j)
            rows.append(values[0])
            ct += values[1]
        
        self.front_ct = ct
        self.card_front = '\n'.join(rows)
    
    def load_back(self):
        rows = []
        ct = 0
        for artifact in self.artifacts:
            data = artifact.__dict__
            if 'BLANK' not in data:
                if str(data['ARTIFACT_COUNT']) == "" or str(data['ARTIFACT_COUNT']).isspace():
                    values = self.format_back(f"{data['ARTIFACT_TYPE']}: {data['ARTIFACT_WEIGHT']}g")
                    rows.append(values[0])
                    ct += values[1]
                else:
                    values = self.format_back(f"{data['ARTIFACT_TYPE']}: ({data['ARTIFACT_COUNT']}) {data['ARTIFACT_WEIGHT']}g")
                    rows.append(values[0])
                    ct += values[1]

        self.back_ct = ct
        self.card_back = '\n'.join(rows)
    
    
    def format_front(self, prefix, string ):
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

        return ['\n'.join(row_ls).replace('@', ' '), len(row_ls)]

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

        return ['\n'.join(row_ls).replace('@', ' '), len(row_ls)]

    def level(self):
        if self.front_ct > self.back_ct:
            for i in range(self.front_ct-self.back_ct):
                self.card_back += '\n '
                self.back_ct = self.front_ct
        elif self.back_ct > self.front_ct:
            for i in range(self.back_ct-self.front_ct):
                self.card_front += '\n '
                self.front_ct = self.back_ct











