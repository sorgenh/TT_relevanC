"""
    WebService pour le test technique RelevanC
    ======================

    Ce webservice contient 3 fonctions pour déclarer des schemas de données, inserer des données en csv
    et les requeter.
    Il supporte 3 types int, string et date. Il est très facile d'ajouter un type, il suffit d'ajouter une fonction
    "check_type_<nom du type>" dans le module ws_utils.
    Il utilise mongoDB.

    Exemple d'usage:
    Un POST sur /test/schema pour déclarer le schema en JSON (Content-Type : application/json)
    Un POST sur /test pour insérer les data (Content-Type : text/plain)
    Un GET sur /test pour récuperer les data au bon format
"""

from flask import Flask
from flask import request
from flask_pymongo import PyMongo

import json
import datetime
now = datetime.datetime.now

from ws_utils import *

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'TT_relevanC'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/TT_relevanC'

mongo = PyMongo(app)


def log(to_log):
    collection = mongo.db['__log']
    collection.insert(to_log)


@app.route('/<nom_schema>/schema', methods=['POST'])
def add_schema(nom_schema):
    """
    Crée une nouvelle collection associée à un schema dans la base.
    Ne remplace pas l'ancien schema si le nom_schema existe déjà.
    Le Content-Type doit être application/json

    :param nom_schema: string
    :return un message décrivant l'action et le code retour http (200 par defaut): string,int
    """
    if nom_schema in mongo.db.collection_names():
        log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "declaration_schema", "statut": "NOK",
             "message": "{} déjà dans la base.".format(nom_schema)})
        return "{} déjà dans la base.".format(nom_schema), 400
    collection = mongo.db[nom_schema]
    request.json["_id"] = "schema"
    collection.insert(request.json)
    log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "declaration_schema", "statut": "OK",
         "message": "Déclaration de {} dans la base.".format(nom_schema)})
    return "Déclaration de {} dans la base.\n".format(nom_schema)+json.dumps(request.json)


@app.route('/<nom_schema>', methods=['POST'])
def add_data(nom_schema):
    """
    Insère des données dans la collection nom_schema.
    Les lignes incomplète ou ne correpondant pas au schema sont ignorées.
    Le Content-Type doit être text/plain

    :param nom_schema: string
    :return un message décrivant l'action et le code retour http (200 par defaut): string,int
    """
    if nom_schema not in mongo.db.collection_names() :
        log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "insertion", "statut": "NOK",
             "message": "{} n'existe pas dans la base.".format(nom_schema)})
        return "{} n'existe pas dans la base. Avez vous déclaré un schéma?".format(nom_schema), 400
    collection = mongo.db[nom_schema]
    schema = collection.find_one({"_id": "schema"})
    del schema["_id"]

    input_data = request.get_data(as_text=True).replace("\r","")
    input_data = input_data.split("\n")
    header = input_data.pop(0)

    if not check_header(schema, header):
        log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "insertion", "statut": "NOK",
             "message": "Le header fournit ne correspond pas au schema."})
        return "Le header fournit ne correspond pas au schema \n {}".format(json.dumps(schema)), 400

    nb_ok = 0
    nb_nok = 0
    for line in input_data:
        if check_line(schema, line):
            collection.insert({"data": line})
            nb_ok += 1
        else:
            nb_nok += 1

    log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "insertion", "statut": "OK",
         "nb_lignes_ok": nb_ok, "nb_lignes_nok": nb_nok})
    return "Nombre de lignes inserées dans le schema {} : {}\n" \
           "Nombre de lignes au mauvais format ou avec valeurs manquantes : {}".format(nom_schema, nb_ok, nb_nok)


@app.route('/<nom_schema>', methods=['GET'])
def get_data(nom_schema):
    """
    Renvoie les données associées à la collection nom_schema

    :param nom_schema: string
    :return un message décrivant l'action et le code retour http (200 par defaut): string,int
    """
    if nom_schema not in mongo.db.collection_names() :
        log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "affichage_donnees", "statut": "NOK",
             "message": "{} n'existe pas dans la base.".format(nom_schema)})
        return "{} n'existe pas dans la base. Avez vous déclaré un schéma?".format(nom_schema), 400
    collection = mongo.db[nom_schema]

    schema = collection.find_one({"_id": "schema"})
    del schema["_id"]

    result = get_header(schema) + "\n"

    cursor = collection.find({"_id": {"$ne": "schema"}})
    for document in cursor:
        if document["_id"] != "schema":
            result += document["data"] + "\n"
    log({"datetime": str(now()), "schema": nom_schema, "type_interaction": "affichage_donnees", "statut": "OK",
         "message": "Affichage des données de {}.".format(nom_schema)})
    return result


if __name__ == '__main__':
    app.run(debug=True,port=5500)
