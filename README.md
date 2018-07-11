WebService pour le test technique RelevanC
======================

Ce webservice contient 3 fonctions pour déclarer des schemas de données, inserer des données en csv
et les requeter.

* POST sur /<nom_schema>/schema pour déclarer le schema en JSON. Le Content-Type doit être application/json
* POST sur /<nom_schema> pour insérer des données au format CSV séparateur |. Les données incomplètes ou ne respectant pas le schema seront ignorées. Le Content-Type doit être text/plain.
* GET sur /<nom_schema> pour récuperer les données, format CSV séparateur |. 

Il supporte 3 types int, string et date. Il est très facile d'ajouter un type, il suffit d'ajouter une fonction
"check_type_\<nom du type\>" dans le module ws_utils.

Il utilise **mongoDB**.
A chaque schema déclaré correpond une collection dans la base TT_relevanC. Chaque collection contient un document avec _id = "schema" contenant le schema associé. Une collection speciale "__log" contient les logs applicatifs d'utilisation du WS.

Exemple d'usage:
* Un POST sur /test/schema pour déclarer le schema en JSON (Content-Type : application/json)
* Un POST sur /test pour insérer les data (Content-Type : text/plain)
* Un GET sur /test pour récuperer les data au bon format