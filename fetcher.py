import yfinance as yf
import sqlite3

conn = sqlite3.connect('mytable1.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Date')



dat = yf.Ticker("RYSAS.IS")
splitData = dat.history(start="2025-01-01", end="2025-12-31").to_dict()


