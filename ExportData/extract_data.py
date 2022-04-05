import os.path
from os.path import isdir
import pyodbc
import pandas as pd
import time
import argparse

server = 'crypto-bot.database.windows.net'
database = 'binance'
username = 'cryptoAdmin'
password = 'Petit@Soleil'
driver = '{ODBC Driver 17 for SQL Server}'

connector_str = 'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' \
                + username + ';PWD=' + password


def query_extract_data(args):

    if args.get('interval'):
        if args.get('limit'):
            query = """
                SELECT 
                TOP {} * 
                FROM future.MarketPrices mp
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                WHERE mp.Symbol = '{}' AND mp.Interval = '{}'
            """.format(args.get('limit'), args.get('cryptoCode'), args.get('interval'))
        else:
            query = """
                SELECT 
                    *
                FROM future.MarketPrices mp 
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                WHERE mp.Symbol = '{}' AND mp.Interval = '{}'
            """.format(args.get('cryptoCode'), args.get('interval'))
    else:
        if args.get('limit'):
            query = """
                SELECT 
                TOP {} * 
                FROM future.MarketPrices mp
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                WHERE mp.Symbol = '{}'
            """.format(args.get('limit'), args.get('cryptoCode'))
        else:
            query = """
                SELECT 
                    *
                FROM future.MarketPrices mp 
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                WHERE mp.Symbol = '{}'
            """.format(args.get('cryptoCode'))
    return query


def shift_past(df_in, nb_timesteps):
    df_out = df_in.copy()
    # On ajoute une colonne à chaque itération
    for k in range(1, nb_timesteps + 1):
        df_out[f"OP_T-{k}"] = df_out["OpenPrice"].shift(k)
    return df_out


def getArguments():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-c", "--cryptoCode", help="Crypto currency Code")
    parser.add_argument("-i", "--interval", help="Candles Interval")
    parser.add_argument("-l", "--limit", help="Number of lines exported")
    parser.add_argument("-p", "--past", help="Number of candles we want to shift from the past in the DF.")

    # Read arguments from command line
    args = parser.parse_args()
    d = vars(args)
    if d.get('limit'):
        try:
            d['limit'] = int(d['limit'])
        except ValueError:
            d['limit'] = None

    if d.get('past'):
        try:
            d['past'] = int(d['past'])
        except ValueError:
            d['past'] = None

    if not d.get('cryptoCode'):
        d['cryptoCode'] = 'BTCBUSD'

    return d


def csv_file_name(args):
    output = "csv_files/"
    if args.get('cryptoCode'):
        output += args.get('cryptoCode')
    else:
        output += 'Crypto'

    if args.get('interval'):
        output += '_' + args.get('interval')

    if args.get('limit'):
        output += '_' + str(args.get('limit')) + 'Lines'

    if args.get('past'):
        output += '_' + str(args.get('past')) + 'PastPrices'

    output += '.csv'
    return output


def welcome_message(args):
    output = f"Export de {args.get('cryptoCode', 'toutes les cryptos')} " \
             f"pour les bougies de {args.get('interval', 'tous les intervalles')} "
    if args.get('limit'):
        output += f"avec une limite de {args.get('limit')} lignes."
    else:
        output += "sans limite de lignes."
    return output


if __name__ == '__main__':
    start = time.time()
    arguments = getArguments()
    print(welcome_message(arguments))

    queryExport = query_extract_data(arguments)

    with pyodbc.connect(connector_str) as conn:
        df = pd.read_sql_query(queryExport, conn)
        df = df.drop('MarketPriceId', axis=1, errors='ignore').sort_values(by=['Interval', 'TimeOpenLong'])

        if arguments.get('past'):
            df_output = shift_past(df, arguments.get('past'))
        else:
            df_output = shift_past(df, 10)

        if os.path.exists("csv_files") and isdir("csv_files"):
            pass
        else:
            os.mkdir("csv_files")

        df_output.to_csv(csv_file_name(arguments), index=False)

    end = time.time()
    print("Temps total : {} sec".format(round(end - start)))
