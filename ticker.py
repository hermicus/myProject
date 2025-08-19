import yfinance as yf
import mysql.connector
import json
import datetime

conn = mysql.connector.connect(
host="localhost",
user="admin",
password="admin",
database="db_name"
)
cur = conn.cursor()

def ticker_insert (check_tick):
    cur.execute('INSERT IGNORE INTO stocks (ticker) VALUES (%s)', (check_tick,))
    conn.commit()

def ticker_fetch (check_tick):
    dat = yf.Ticker(check_tick)
    test_dat = dat.history(period="1mo")
    if test_dat.empty:
        raise Exception("Invalid Ticker Symbol")
    else:
        return check_tick
try:
    check_tick = input("Enter the ticker symbol: ")
    ticker_val = ticker_fetch(check_tick)
    ticker_insert(ticker_val)
except Exception as e:
    print(e)

print("finished")