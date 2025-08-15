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

def ticker_insert ():
    check_tick = input("Enter the ticker symbol: ")
    dat = yf.Ticker(check_tick)
    test_dat = dat.history(period="1mo")
    if test_dat.empty:
        print("Invalid Ticker Symbol")
    else:
        cur.execute('INSERT IGNORE INTO stocks (ticker) VALUES (%s)', (check_tick,))


check = yf.Ticker("CHFTRY=X")
check2 = check.history(period="1mo")
ticker_insert()
print("finished")