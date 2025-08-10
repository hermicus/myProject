import yfinance as yf
import sqlite3
import json

from websockets import Close

#Dumping and creating fresh tables for testing purposes

conn = sqlite3.connect('mysql1.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS stocks;
DROP TABLE IF EXISTS currency;
DROP TABLE IF EXISTS prices;

CREATE TABLE "currency" (
	"id"	INTEGER NOT NULL UNIQUE,
	"Currency"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "stocks" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ticker"	TEXT NOT NULL,
	"basis_currency_id"	integer NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "prices" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	INTEGER NOT NULL,
	"currency_id"	INTEGER NOT NULL,
	"stock_id"	INTEGER NOT NULL,
	"close_price"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''')

conn.commit()

#Adding base data for the fetching

cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )


temp_list = cur.execute('SELECT ticker FROM stocks')
for row in temp_list:
    dat = yf.Ticker(str(row[0]))
    fname = dat.history(start="2025-01-01", end="2025-01-31")
    strData = fname.to_json()
    jsonData = json.loads(strData)
    for entry in jsonData.items()["Close"]:
        CloseData = entry[0:]
        print(CloseData)

conn.commit()

cur.close()

# Changing date to list and then adding to DB + whiling through the values
# Or somehow using items to update SQL ?