"""
WS_Utils : Module contenant les fonctions necessaire pour le WebService RelevanC
"""

import sys
from datetime import datetime

SEPARATEUR="|"


def check_header(schema, header):
    """
    :param schema: dictionnaire
    :param header: liste
    :return True si le header correspond au schema, False sinon: booleen
    """
    header_tab = header.split(SEPARATEUR)
    if len(schema) != len(header_tab):
        return False
    for i in range(len(schema)):
        if list(schema.keys())[i] != header_tab[i]:
            return False
    return True


def get_header(schema):
    """
    :param schema: dictionnaire
    :return Le header csv correpondant au schema: string
    """
    return SEPARATEUR.join(schema.keys())


def check_line(schema, line):
    """
    Vérifie si une ligne correpond au schema dans lequel on compte l'inserer, verification du remplissage
    des champs et de leur types.
    :param schema: dictionnaire
    :param line: string
    :return True or False:
    """
    line_tab = line.split(SEPARATEUR)
    if len(schema) != len(line_tab):
        return False
    for i in range(len(schema)):
        if not check_type(list(schema.values())[i], line_tab[i]):
            return False
    return True


def check_type(type_to_check, data):
    """
    Vérifie si la string fournie correspond a un type.
    Fonctionne grâce à la reflexivité de Python
    :param type_to_check: type attendu
    :param data: donnée à evaluer
    :return True or False:
    """
    return getattr(sys.modules[__name__], 'check_type_'+type_to_check)(data)


def check_type_string(data):
    """
    :param data: string
    :return True si non vide, False sinon:
    """
    return data != ""


def check_type_int(data):
    """
    :param data: string
    :return True si représente un entier, False sinon:
    """
    try:
        int(data)
        return True
    except ValueError:
        return False


def check_type_date(data):
    """
    :param data: string
    :return True si représente une date au format %Y-%m-%d, False sinon:
    """
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False
