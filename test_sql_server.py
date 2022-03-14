import pyodbc


server = 'crypto-bot.database.windows.net'
database = 'binance'
username = 'cryptoAdmin'
password = 'Petit@Soleil'
driver='{ODBC Driver 18 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT name FROM sys.tables")
        row = cursor.fetchall()
        print(row)