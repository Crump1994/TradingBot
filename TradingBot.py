import requests
import yfinance as yf
import mysql.connector
import sqlalchemy
import mysql.connector

url = "https://demo.trading212.com/api/v0/equity/account/info"
headers = {"Authorization": "31597166ZMLDVBQxzrVQGIrgWEzESOoyAkhgX"}

aapl= yf.Ticker("aapl")
tsla= yf.Ticker("TSLA")

aapl_historical = aapl.history(start="2024-03-21", end="2024-03-22", interval="1m")
tslaHist = tsla.history(start="2024-03-22", end="2024-03-23", interval="5m")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Password",
  database="apple22032024"
)


def createTable():
    database_username = 'root'
    database_password = 'Password'
    database_ip       = 'localhost'
    database_name     = 'apple22032024'

    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(database_username, database_password, 
                                                        database_ip, database_name))
    tslaHist.to_sql(con=database_connection, name='price', if_exists='replace')


def trader():
    budget = 5000
    stock = 0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Open, High, Low, Close  FROM price")
    myResult = mycursor.fetchall()



    count = 0
    lossCount = 0
    gainCount = 0


    lastNum = len(myResult)-1
    lastSell = False
    buy = False
    sellPrice = 0.0
    lastBuyPrice = 0
    for price in myResult:

        lastPrice = myResult[count-1]

        if buy == True and budget > price[0] and lastSell == False:
            budget = budget - price[0]
            stock = stock + 1
            buy = False
            sellPrice = lastPrice[0]
            print("I bought here for " + str(price[0]))
            print("The lowest I should sell for is " + str(sellPrice))
            print("I have " + str(stock) + " stock")

        if stock > 0 and sellPrice < price[0]:
            sellPrice = price[0]
        elif stock > 0:
            budget = budget + (stock * price[0])
            print(budget)
            stock = 0
            print("I sold here for " + str(price[0]))
            if count > lastNum - 18:
                lastSell = True


        

        if (count > 0 and lastPrice[0] > lastPrice[3] and price[0] > lastPrice[3] and price[3] > lastPrice[0]):
            buy = True
        count = count + 1
        print(price)
    
    LastStock = myResult[lastNum]
    budget = budget + (stock * LastStock[0])
    print("I sold here for " + str(LastStock[0]))
    print(budget)

createTable()
trader()
    