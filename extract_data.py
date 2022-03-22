import pyodbc
import pandas as pd
import time
import argparse

server = 'crypto-bot.database.windows.net'
database = 'binance'
username = 'cryptoAdmin'
password = 'Petit@Soleil'
driver = '{SQL Server}'

connector_str = 'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' \
                + username + ';PWD=' + password


def extract_data(args):
    if args.get('interval'):
        if args.get('limit'):
            query = """
                SELECT 
                TOP {} * 
                FROM future.MarketPrices mp
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId
                WHERE mp.Symbol = '{}' AND mp.Interval = '{}'
            """.format(args.get('limit'), args.get('cryptoCode'), args.get('interval'))
        else:
            query = """
                SELECT 
                    *
                FROM future.MarketPrices mp 
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId
                WHERE mp.Symbol = '{}' AND mp.Interval = '{}'
            """.format(args.get('cryptoCode'), args.get('interval'))
    else:
        if args.get('limit'):
            query = """
                SELECT 
                TOP {} * 
                FROM future.MarketPrices mp
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId
                WHERE mp.Symbol = '{}'
            """.format(args.get('limit'), args.get('cryptoCode'))
        else:
            query = """
                SELECT 
                    *
                FROM future.MarketPrices mp 
                LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
                LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId
                WHERE mp.Symbol = '{}'
            """.format(args.get('cryptoCode'))
    return query


def generate_dataset(df, nb_timesteps):
    df_output = df.copy()
    # On ajoute une colonne à chaque itération
    for k in range(1, nb_timesteps + 1):
        df_output[f"0P_T-{k}"] = df_output["OpenPrice"].shift(k)
    return df_output


def getArguments():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-c", "--cryptoCode", help="Crypto currency Code")
    parser.add_argument("-i", "--interval", help="Candles Interval")
    parser.add_argument("-l", "--limit", help="Number of lines exported")

    # Read arguments from command line
    args = parser.parse_args()
    d = vars(args)
    if d.get('limit'):
        try:
            d['limit'] = int(d['limit'])
        except ValueError:
            d['limit'] = None
    return d


def csv_file_name(args):
    output = ""
    if args.get('cryptoCode'):
        output += args.get('cryptoCode')
    else:
        output += 'Crypto'

    if args.get('interval'):
        output += '_' + args.get('interval')

    if args.get('limit'):
        output += '_' + str(args.get('limit')) + 'Lines'

    output += '.csv'
    return output


if __name__ == '__main__':
    start = time.time()

    arguments = getArguments()
    query = extract_data(arguments)

    with pyodbc.connect(connector_str) as conn:
        df = pd.read_sql_query(query, conn)
        df = df.drop('MarketPriceId', axis=1, errors='ignore').sort_values(by=['Interval', 'TimeOpenLong'])
        df.to_csv('first_test_BTC.csv')
        df_output = generate_dataset(df, 25)
        file_name = csv_file_name(arguments)
        df_output.to_csv(file_name, index=False)

    end = time.time()
    print("Temps total : {} sec".format(round(end - start)))
