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
        d = gf.copy_dict(bag.__dict__, ['artifact_ls'])
        ls = self.dict_to_ls(d)
        self.pref = ls[1]
        self.front_ls = ls[0]
        self.back_ls = []

        if type(bag.artifact_ls) == dict:
            bag.artifact_ls = [bag.artifact_ls]
        for i in bag.artifact_ls:
            self.back_ls.append(i.string)

        ls = self.format(self.front_ls, False)
        self.front_ls = ls[0]
        self.f_ct = ls[1]
        self.f_pre = ls[2]

        ls = self.format(self.back_ls, True)
        self.back_ls = ls[0]
        self.b_ct = ls[1]
        self.b_pre = ls[2]

        self.level()

        self.front_str = gf.replace_chars(''.join(self.front_ls))

        self.back_str = gf.replace_chars(''.join(self.back_ls))

    def format(self, ls, back):
        return_ls = []
        ct = 0

        for i in ls:
            pre_ls = []
            temp_ls = []
            temp_str = ''
            return_str = ''
            split_ls = i.split(' ')

            flag = True
            for j in split_ls:
                
                temp_str = ' '.join(temp_ls)

                if len(temp_str) + len(j) >= 28:
                    return_str += f"{temp_str}\n"
                    temp_ls = ['      ']
                    ct += 1
                    flag = True
                temp_ls.append(j)
                if ':' in ' '.join(temp_ls):
                    pre_ls.append(' '.join(temp_ls))
                    for x in range(22):
                        pre_ls[-1] += ' '
                    flag = False

            return_str += f"{' '.join(temp_ls)}\n"
            return_ls.append(return_str)
            ct += 1
        # for spacing
        if back == True:
            return_ls.insert(0, ' \n')
            ct += 1
        else:
            return_ls.append(' \n')
            ct += 1

        try:
            return [return_ls, ct, pre_ls[0]]
        except:
            return [return_ls, ct, ['g']]
    
    def level(self):
        diff = self.f_ct - self.b_ct

        if diff > 0:
            for i in range(diff):
                if self.back_ls:
                    self.back_ls[-1] += '\n'
                else:
                    self.back_ls.append('\n')
            self.newln_ct = self.f_ct

        elif diff < 0:
            for i in range(abs(diff)):
                if self.front_ls:
                    self.front_ls[-1] += '\n'
                else:
                    self.front_ls.append('\n')
            self.newln_ct = self.b_ct
        else:
            pass

    # Returns list with formatted prefixes
    def dict_to_ls(self, dictionary):
        temp_ls = []
        temp_ls_2 = []

        dictionary.pop('BAG_INDEX', None)
        for k, v in dictionary.items():
            if v != '':
                temp_ls_2.append("%s                     " % self.format_prefix(k))
                temp_ls.append("%s %s" % (self.format_prefix(k), v))
                if temp_ls[-1][-1] != ';':
                    temp_ls[-1]+= ';'
        return [temp_ls, temp_ls_2]

    #Returns formatted card label prefix string according to character limit + colon 
    def format_prefix(self, string):
        char_limit = 5

        if len(string) > char_limit:
            string = string[0:5]

        string += ':'
        for i in range(char_limit - len(string) + 1):
            string += ' '
        
        return string














