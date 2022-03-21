import pyodbc
import pandas as pd
import time

server = 'crypto-bot.database.windows.net'
database = 'binance'
username = 'cryptoAdmin'
password = 'Petit@Soleil'
driver = '{SQL Server}'

connector_str = 'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' \
                + username + ';PWD=' + password


def extract_data(cryptoCode, limit=None):
    if limit:
        query = """
            SELECT 
            TOP {} * 
            FROM future.MarketPrices mp
            LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
            LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId
            WHERE mp.Symbol = '{}'
        """.format(limit, cryptoCode)
    else:
        query = """
            SELECT 
                *
            FROM future.MarketPrices mp 
            LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId
            LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId
            WHERE mp.Symbol = '{}'
        """.format(cryptoCode)
    return query


if __name__ == '__main__':
    start = time.time()
    with pyodbc.connect(connector_str) as conn:
        query = extract_data('BTCBUSD')
        df = pd.read_sql_query(query, conn)
        print(df.head())
        df.to_csv('first_test_BTC.csv')

    end = time.time()
    print("Temps total : {} sec".format(round(end - start)))