from datetime import date
import pandas as pd
import os.path

header = """<html>
<head>
    <title>{}</title>

    <style>
        body {{
            background-color = white;
        }}

        p {{
            font-family: 'Courier', 'Courier New', monospace;
            color: black;
        }}

        hr {{
            width: 220px;
            text-align: left;
            margin-left: 0;
        }}

        .siteBox {{
            border-left: 6px solid dimgrey;
            
        }}

        .invBox {{
            border-left: 6px solid lightgrey;
        }}

        .provCatBox {{
            border-left: 6px solid forestgreen;
        }}

        .remBox {{
            border-left: 6px solid #CD5C5C;
        }}
        
        p.regular {{
            font-weight: 400;
        }}

        p.bold {{
            font-weight: 900;
        }}
    </style>
    
</head>
<body>
</body>
</html>
"""

def sbox(msg):
    return '<p style="margin: 0"><span class="siteBox">&ensp;Site Number:&ensp;<span style="font-weight: 900">{}</span></span></p>'.format(msg)

def ibox(msg):
    return '<p style="margin: 0"><span class="invBox">&ensp;Inv. Number:&ensp;<span style="font-weight: 900">{}</span></span></p>'.format(msg)

def preg(msg):
    return '<p class="regular">{}</p>'.format(msg)

def pcBox(msg):
    return '<p><span class="provCatbox"><span style="font-weight: 900">{}</span></p>'.format(msg)

def rmBox(msg):
    return '<p><span class="remBox"><span style="font-weight: 900">{}</span></p>'.format(msg)

def pbold(msg):
    return '<p class="bold">{}</p>'.format(msg)

def write_html(filename, site, inv, prov_ls, cat_ls, art_ls):
    #file = open(filepath_sep+"/%s.html" % filename, 'w+')
    file = open(f"file_output\{filename}.html", 'w+')

    if prov_ls == []:
        prov_ls = ['No provenience information']
    if cat_ls == []:
        cat_ls = ['No catalogue numbers']
    cats_ls = pd.Series(cat_ls)      
    provs_ls = pd.Series(prov_ls)
    
    provs_ls = provs_ls.replace("’", "&apos;", regex=True)
    provs_ls = provs_ls.replace("”", "&quot;", regex=True)

    #Write date/time, filename
    file.write(preg(date.today().strftime("%B %d, %Y")))
    file.write(sbox("&ensp;%s&ensp;" % site))
    file.write(ibox("&ensp;%s&ensp;" % inv))
    file.write("<hr>")

    #Write provenience
    file.write(pcBox("&ensp;Provenience&ensp;"))

    file.write(preg(provs_ls.to_string(index=False)))

    #Write catalogue numbers
    file.write(pcBox("&ensp;Catalogue Numbers&ensp;"))
    file.write(preg(cats_ls.to_string(index=False)))

    #Write Artifacts
    file.write(pcBox("&ensp;Artifacts&ensp;"))
    for i in art_ls:
        file.write(preg(f"{i[0]}: ({i[1]}) {i[2]}g"))
    
    file.write(header.format(""))

