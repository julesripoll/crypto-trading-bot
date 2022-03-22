# crypto-trading-bot

Trading bot using alpaca api, aws and python.

## Exporter les données depuis la base de données

Pour exporter les données depuis SQL Server, lancez le script `extract_data.py`. Pour spécifier le type de données à extraire, vous pouvez utiliser les arguments suivants :
* `--cryptoCode` ou `-c` : le code de la cryptomonnaie à extraire.
* `--interval` ou `-i` : l'interval des bougies.
* `--limit` ou `-l` : pour limiter le nombre de lignes à extraire.

Exemples :
* `python extract_data.py` : exporter toutes les données de la base.
* `python extract_data.py -c 'BTCBUSD' -i '1m' -l 50` : exporter les données du BTC/BUSD, pour les bougies de 1 minute et se limiter à 50 lignes.
* `python extract_data.py --cryptoCode 'BTCBUSD' --interval '1d'` : exporter les données du BTC/BUSD, pour les bougies journalières.
* etc...

La sortie est un fichier CSV nommé en fonction des arguments passés au script.