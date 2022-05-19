# crypto-trading-bot

Trading bot using alpaca api, aws and python.

To-Do board : https://trello.com/b/gbe9xqEX/sprint-0

## Exporter les données depuis la base de données

Pour exporter les données depuis SQL Server en utilisant Docker, il faut :
* se placer dans le dossier `ExportData/`.
* builder l'image Docker : `docker build -t exportdata .` (Ne pas oublier le `.`).
* lancer le container : `docker run --rm -v ${PWD}/csv_files/:/app/csv_files exportdata {args}` avec `args` les arguments de l'export.

Les arguments utilisables sont :
* `--cryptoCode` ou `-c` : le code de la cryptomonnaie à exporter (si vide alors BTC).
* `--interval` ou `-i` : l'intervalle des bougies.
* `--limit` ou `-l` : pour limiter le nombre de lignes à exporter.
* `--past` ou `p` : choisir le nombre de bougies du passé à shifter.

Exemples :
* `docker run ... exportdata` : exporter toutes les données de la base avec du BTC.
* `docker run ... exportdata -c 'BTCBUSD' -i '1m' -l 50` : exporter les données du BTC/BUSD, pour les bougies de 1 minute et se limiter à 50 lignes.
* `docker run ... exportdata --cryptoCode 'ETHBUSD' --interval '1d'` : exporter les données du ETH/BUSD, pour les bougies journalières.
* etc...

La sortie est un fichier CSV nommé en fonction des arguments passés au script. Ce fichier se trovue dans le dossier `csv_files/`.


A venir : script bash pour simplifier les commandes à lancer.
