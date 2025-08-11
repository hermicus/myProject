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
	"currency"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "stocks" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ticker"	TEXT NOT NULL,
	"base_currency_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
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

cur.executescript('''INSERT OR IGNORE INTO stocks (ticker, base_currency_id) VALUES ("RYSAS.IS", 1);

INSERT OR IGNORE INTO currency (currency) VALUES ("TRY");
''')

conn.commit()


temp_list = cur.execute('SELECT ticker FROM stocks')
for row in temp_list:
    dat = yf.Ticker(str(row[0]))
    fname = dat.history(start="2025-01-01", end="2025-01-31", auto_adjust=False)
    strData = fname.to_json()
    jsonData = json.loads(strData)

# loop through json to add to mysql

for key, value in jsonData["Adj Close"].items():
	print(key, value)
	sql = "INSERT or IGNORE INTO prices (close_price, date) VALUES (?, ?)"
	cur.execute(sql, (value, key))
	conn.commit()



cur.close()


