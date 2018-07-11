


SEPARATEUR="|"

def check_header(schema, header):
    header_tab = header.split(SEPARATEUR)
    if len(schema) != len(header_tab):
        return False
    for i in range(len(schema)):
        if list(schema.keys())[i] != header_tab[i]:
            return False
    return True
