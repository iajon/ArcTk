import json
import copy

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



