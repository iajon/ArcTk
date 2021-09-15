import pandas as pd
import numpy as np

from sql.queries import Connection

import lib.GeneralFunctions as gf
from lib.Classes import Artifact, ArtifactType, Bag

# Drops columns from dataframe according to dictionary value
def drop_columns(dataframe, dictionary, key):
    for i in dictionary:
        value = dictionary.get(i)

        if value == key:
            dataframe = dataframe.drop(dataframe.columns[int(i)], axis = 1)

    return dataframe

# Appends blank strings to column prefix dictionary, match dict length to column num
def append_column_prefixes(column_len, dictionary):
    for i in range(column_len - len(dictionary)):
        inc = i + len(dictionary)
        dictionary[str(inc)] = 'Unnamed_' + str(inc)
    
    return dictionary

# Creates list of bag objects from dataframe
def get_bag_list(dataframe):

    # Information for front of card
    info_dict = {}

    # Information for back of card
    artifact_dict = {}

    # Carries multiple Artifact(**artifact_dict)
    artifact_ls = []

    # Carries multiple Bag(**info_dict, artifact_ls = artifact_ls)
    bag_ls = []

    # Row incrementer for artifacts of same bag
    x = 1

    for i in range(len(dataframe)):
        info_dict = {}
        cat_ls = []
        artifact_dict = {}
        artifact_ls = []
        
        x = 1

        # If row has unique id (keep info)
        if str(dataframe.iloc[i]['BAG_INDEX']) != '0' and str(dataframe.iloc[i]['BAG_INDEX'])[0:6] != '/Site:':
            
            info_dict = dataframe.iloc[i].to_dict()
            

            keys = list(reversed(list(info_dict)))[0:3]
            for j in list(reversed(keys)):
                artifact_dict[j] = info_dict[j]
                info_dict.pop(j, None)
            try:
                info_dict['Site'] = site
            except:
                pass
            artifact_ls.append(Artifact(**artifact_dict))

            # If subsequent rows DO NOT have unique id (include in prev. info)
            try:
                while int(dataframe.iloc[i+x]['BAG_INDEX']) == 0:
                    temp_dict = dataframe.iloc[i+x].to_dict()

                    for k in list(temp_dict)[0:6]:
                        temp_dict.pop(k, None)
                    
                    artifact_ls.append(Artifact(**temp_dict))
                    x += 1
            except:
                pass
            # Append info + list of artifacts to bag_ls (list of bags)
            bag_ls.append(Bag(**info_dict, artifact_ls = artifact_ls))

        elif str(dataframe.iloc[i]['BAG_INDEX'])[0:6] == '/Site:':
            site = str(dataframe.iloc[i]['BAG_INDEX'])[6:]
            
    for i in bag_ls:
        if i.card.newln_ct == 0:
            i.card.newln_ct = 2
    return bag_ls

# Returns dataframe initialized w/ json preferences
def init_dataframe(filepath, column_prefs, header_row, last_column):

    # Set pandas preferences
    pd.set_option('display.max_colwidth', None)

    # Initialize dataframe
    dataframe = pd.read_excel(filepath)
    
    # Set header row
    column_names = append_column_prefixes(len(dataframe.columns), column_prefs)
    column_names = list(column_prefs.values())
    dataframe = pd.DataFrame(dataframe.values[header_row:], columns = column_names)

    # Drop columns according to json preferences
    dataframe = drop_columns(dataframe, column_prefs, key = '')

    # Grab columns from [0, last_column minus number of columns dropped according to column_prefs]
    drop_count = gf.value_count(column_prefs, '')
    dataframe = dataframe.loc[:, :dataframe.columns[last_column-drop_count]]

    #Drop all NaN
    dataframe = dataframe.dropna(how='all')
    dataframe = dataframe.replace(np.nan, '', regex=True)
    dataframe['BAG_INDEX'] = dataframe['BAG_INDEX'].replace('', 0, regex=True)

    return dataframe

def get_artifact_df(df):
    art_list = ['Empty', 'Debitage', 'Utilized Debitage', 'Biface', 'Hafted Biface - Side Notch', 'Hafted Biface - Corner Notch', 'Hafted Biface - Basal Notch', 'Hafted Biface - Stemmed', 'Hafted Biface - Lanceolate', 'Axe', 'Adze', 'Core', 'Drill', 'Uniface', 'Misc. Chipped Stone', 'Groundstone', 'Abrader', 'Mano', 'Metate', 'Nuttingstone', 'Hammerstone', 'Hematite', 'Lead', 'Ochre', 'Limonite', 'FCR Weight', 'Sandstone', 'Limestone', 'Unmodified Stone', 'Misc. Stone', 'Charcoal', 'Wood', 'Seed', 'Nutshell', 'Textile', 'Misc. Botanical', 'Animal Bone', 'Shell', 'Bead', 'Button', 'Misc. Faunal', 'Whiteware', 'Stoneware', 'Earthenware', 'Procelain', 'Other Historic', 'Unidentified', 'Brick', 'Mortar', 'Misc. Historic', 'Sherd', 'Sherd Body', 'Sherd Rim', 'Vessel', 'Pipe', 'Stem', 'Fired Clay', 'Other Prehistoric', 'Unidentified', 'Misc. Prehistoric', 'Sample', 'Nail', 'Utensil', 'Horseshoe', 'Button', 'Gun Parts', 'Bullet', 'Casing', 'Misc. Metal', 'Container Fragments', 'Whole Container', 'Bead', 'Button', 'Misc. Glass', 'Plastic', 'Rubber', 'Other Misc.', 'Unidentified']
    art_dict = {i:[0, 0.0] for i in art_list}

    df.fillna(0, inplace=True)
    
    # Fill art_dict with values
    for index, row in df.iterrows():
        try:
            art_dict[row['artifact_type_name']][0] += row['artifact_count']
        except:
            pass
        try:
            art_dict[row['artifact_type_name']][1] += row['artifact_weight']
        except:
            pass
    
    # Copy only non-zero count & weight
    data = []
    for k,v in art_dict.items():
        if v[1] == 0.0:
            pass
        elif v[0] == 0:
            data.append([k, '>10 or N/A', v[1]])
        else:
            data.append([k, v[0], v[1]])

    # Data to df
    df = pd.DataFrame(data, columns=['Artifact Type', 'Count Total', 'Weight Total (g)'])
    return df
    

    
    
