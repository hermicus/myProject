import yfinance as yf
import sqlite3
import json
import datetime

from websockets import Close

#Dumping and creating fresh tables for testing purposes
today = datetime.datetime.today().date()
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
	"ticker"	TEXT NOT NULL Unique,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "prices" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	INTEGER NOT NULL,
	"stock_id"	INTEGER NOT NULL,
	"close_price"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''')

conn.commit()

#Adding base data for the fetching

cur.executescript('''INSERT OR IGNORE INTO stocks ( ticker ) VALUES ("RYSAS.IS"),("RYGYO.IS"), ("AGESA.IS");

INSERT OR IGNORE INTO currency (currency) VALUES ("TRY");
''')

conn.commit()

#Load all the tickers in de DB to a list

temp_list = cur.execute('SELECT ticker, id FROM stocks').fetchall()
for row in temp_list:
	stock_id = row[1]
	dat = yf.Ticker(str(row[0]))
	fname = dat.history(start="2025-01-01", end=str(today), auto_adjust=False)
	rawData = fname.to_json()
	jsonData = json.loads(rawData)

	#Fetch all adjusted closing date and insert them one by one into de DB

	for key, value in jsonData["Adj Close"].items():
		sql = "INSERT or IGNORE INTO prices (close_price, date, stock_id) VALUES (?, ?, ?)"
		cur.execute(sql, (value, key, stock_id))
conn.commit()

cur.close()

def my_updater():
	ticker_to_update = cur.execute('SELECT ticker, id FROM stocks').fetchall()

