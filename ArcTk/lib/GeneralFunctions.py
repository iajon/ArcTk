import json
import copy

import natsort as ns
from natsort import natsorted

# Checks if key is in dictionary and returns True or False   
def check_key(dictionary, key):
    if key in dictionary.keys():
        return True
    else:
        return False

# Returns copy of dictionary with k,v pairs removed
def copy_dict(dictionary, keys_to_remove):
    temp_dict = copy.deepcopy(dictionary)

    for i in keys_to_remove:
        temp_dict.pop(i, None)

    return temp_dict

# Returns count of how many times a value appears
def value_count(dictionary, value):
    return list(dictionary.values()).count(value)

# Returns dictionary from json file
def get_json_prefs(filename, key):

    f = open(filename,)
    data = json.load(f)
    f.close()

    return data[str(key)]

#Replacements (for use if multiple replacements are needed in future)
def replace_chars(s):
    s = s.replace("’", "'")
    s = s.replace('”', '"')
    
    return s

def get_cat_nums(ls):
    new_ls = []

    temp_str = ''
    temp_ls = []
    for i in ls:
        temp_str = i.__dict__['Cat#']
        temp_str = temp_str.replace(';', ' ')
        temp_ls = temp_str.split()
        for x in temp_ls:
            new_ls.append(x)
    res = []
    for i in new_ls:
        if i not in res:
            res.append(i)

    new_ls = natsorted(res, alg=ns.IGNORECASE)
    return new_ls

def get_prov_ls(ls):
    new_ls = []

    for i in ls:
        temp_str = i.__dict__['Prov']
        temp_str = temp_str.strip()
        if temp_str != '':
            if temp_str[-1] == ';':
                temp_str[-1].pop()
            new_ls.append(temp_str)
    res = []
    for i in new_ls:
        if i not in res:
            res.append(i)
    return natsorted(res, alg=ns.IGNORECASE)



