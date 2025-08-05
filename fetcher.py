import yfinance as yf
import sqlite3
import json

from websockets import Close

conn = sqlite3.connect('mysql1.sqlite')
cur = conn.cursor()
#cur.execute('ALTER TABLE stocks ADD basis_currency_id integer;')

conn.commit()

temp_list = cur.execute('SELECT ticker FROM stocks')
for row in temp_list:
    dat = yf.Ticker(str(row[0]))
    fname = dat.history(start="2025-01-01", end="2025-01-31")
    strData = fname.to_json()
    jsonData = json.loads(strData)
    for entry in jsonData.items()["Close"]:
        CloseData = entry[0:]
        print(CloseData)


cur.close()

# Changing date to list and then adding to DB + whiling through the values
# Or somehow using items to update SQL ?