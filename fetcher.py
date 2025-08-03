import yfinance as yf
import sqlite3
from datetime import datetime

conn = sqlite3.connect('mysql1.sqlite')
cur = conn.cursor()
#cur.execute('ALTER TABLE stocks ADD basis_currency_id integer;')

conn.commit()

temp_list = cur.execute('SELECT ticker FROM stocks')
for row in temp_list:
    dat = yf.Ticker(str(row[0]))
    splitData = dat.history(start="2025-01-01", end="2025-12-31")
    splitData = splitData.to_json()
    print(splitData)
    #print(dir(dat.history()))


cur.close()

