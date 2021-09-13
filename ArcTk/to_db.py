import lib.ExcelFunctions as xlf
import lib.GeneralFunctions as gf

from sql.queries import Connection

column_prefixes = gf.get_json_prefs('ExcelPreferences.json', 'column_prefixes')
header_row = gf.get_json_prefs('ExcelPreferences.json', 'header_row')
last_column = gf.get_json_prefs('ExcelPreferences.json', 'last_column')

dataframe = xlf.init_dataframe('23FR170_Main_2.xlsx', column_prefixes, int(header_row), int(last_column))
bag_ls = xlf.get_bag_list(dataframe)

print(bag_ls)
con = Connection('database.db')

for i in bag_ls:
    con.insert_bag(i)
3