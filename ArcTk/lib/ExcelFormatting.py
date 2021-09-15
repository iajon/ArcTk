def format_cat(s):
    if s == '':
        return s
    else:
        s = s.strip()
        s = s.replace(';', ' ')

        ls = s.split()
        ls = '; '.join(ls) + ';'

        return ls
    
def format_prov(s):
    if s == '':
        return s
    else:
        s = s.strip()
        if s[-1] != ';':
            s += ';'
    
        return s