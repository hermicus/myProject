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

#Dumping and creating fresh tables for testing purposes
today = datetime.datetime.today().date()

cur = conn.cursor()



# Drop tables
cur.execute('DROP TABLE IF EXISTS prices')
cur.execute('DROP TABLE IF EXISTS stocks')
cur.execute('DROP TABLE IF EXISTS currency')

# Create tables
cur.execute('CREATE TABLE currency (id INT AUTO_INCREMENT PRIMARY KEY, currency VARCHAR(3))')
cur.execute('CREATE TABLE stocks (id INT UNIQUE AUTO_INCREMENT PRIMARY KEY, ticker VARCHAR(100) UNIQUE)')
cur.execute('CREATE TABLE prices (id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY, date INT NOT NULL, stock_id INT NOT NULL, close_price DECIMAL(20,6) NOT NULL)')

# Insert base data
cur.execute('INSERT IGNORE INTO stocks (ticker) VALUES ("RYSAS.IS"), ("RYGYO.IS"), ("AGESA.IS")')
cur.execute('INSERT IGNORE INTO currency (currency) VALUES ("TRY")')

conn.commit()
cur.reset()

#Load all the tickers in de DB to a list

cur.execute('SELECT ticker, id FROM stocks')
temp_list = cur.fetchall()
for row in temp_list:
	stock_id = row[1]
	dat = yf.Ticker(str(row[0]))
	fname = dat.history(start="2025-01-01", end=str(today), auto_adjust=False)
	rawData = fname.to_json()
	jsonData = json.loads(rawData)

	#Fetch all adjusted closing date and insert them one by one into de DB

	for key, value in jsonData["Adj Close"].items():
		sql = "INSERT IGNORE INTO prices (close_price, date, stock_id) VALUES (%s, %s, %s)"
		cur.execute(sql, (value, int(key), stock_id))
		conn.commit()


cur.close()
conn.close()

def my_updater():
	ticker_to_update = cur.execute('SELECT ticker, id FROM stocks').fetchall()

