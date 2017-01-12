#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle, sys, os
from getch import getch
from poloniex import Poloniex

def new():
    print "Welcome to Cryptfolio, a CLI cryptocurrency portfolio!\nStart by adding a position. To keep things simple, all altcoin prices must be entered in terms of BTC."
    coin = addCoin()
    return coin

def menu():

    while True:
        print "Main menu"
        print "1| Dashboard\n2| Manage coins\n3| Exit"
        x = int(getch())
        if x == 1:
            dashboard()
        elif x == 2:
            manageCoins()
        elif x == 3:
            sys.exit()
        else:
            print "Invalid choice.\n"

def dashboard():

    while True:
        print "\nDashboard"
        print "1| Current Prices\n2| Your Positions\n3| Back"
        l = int(getch())

        if l == 1:
            print ''
            prices()
        elif l == 2:
            showCoins(0)
        elif l == 3:
            print ''
            break
        else:
            print "Invalid choice.\n"

def prices():
    
    duplicates = [] # for making sure the same coin isn't printed twice
    print "Current Prices"
    ticker = polo.returnTicker()

    for coin in coins:
        if coin.symbol not in duplicates: # checks to see if the coin has been printed already
            duplicates.append(coin.symbol) 
            if coin.symbol != 'BTC':
                data = ticker['BTC_'+coin.symbol]
            else:
                data = ticker['USDT_'+coin.symbol]
            price = float(data['last']) # gets last price
            change = float(data['percentChange']) * 100 # gets 24hr % change
            if coin.symbol != 'BTC':
                print "%s is at %f฿, a change of %.2f%s" % (coin.symbol, price, change, '%')
            else:
                print "%s is at $%.2f, a change of %.2f%s" % (coin.symbol, price, change, '%')
        else:
            pass

def manageCoins():

    while True:
        print "\nCoin Managment"
        print "1| Add\n2| Delete\n3| Modify\n4| Back"
        y = int(getch())

        if y == 1:
            addCoin()
        elif y == 2:
            delCoin()
        elif y == 3:
            modCoin()
        elif y == 4:
            pickle.dump(coins, open("coins", "wb"))
            print ""
            break
        else:
            print "Invalid choice"
    

def addCoin():
    symbol = raw_input("\nSymbol: ").upper()
    amount = input("Amount: ")
    price = input("Price: ")
    coin = Coin(symbol, amount, price) # creates new coin object
    coins.append(coin) # adds it to list of coins
    return coin

def delCoin():
    
    showCoins(1)
    while True:
        z = raw_input("Chose the number of the position you want to delete or type 'back': ")
        if z == 'back':
            break
        else:
            z = int(z)
        try:
            del coins[z-1] # deletes coin
            break
        except:
            print "Index out of range."

def modCoin():
    
    showCoins(1)
    while True:
        v = raw_input("Chose the number of the position you want to modify or type 'back': ")
        if v == 'back':
            break
        else:
            v = int(v)

        print "\n1|Amount\n2|Price\n3|Back"
        w = int(getch())
        if w == 1:
            newAmnt = input("Enter new amount: ")
            try:
                coins[v-1].amount = newAmnt # changes coin amount
            except:
                "Error: index out of range or invalid number."
        elif w == 2:
            newPrice = input("Enter new price: ")
            try:
                coins[v-1].price = newPrice # changes coin price
            except:
                "Error: index out of range or invalid number."
        elif w == 3:
            break
        else:
            print "Invalid option."
        
        break


def showCoins(n):
    
    print ""
    if n == 1:
        print "Positions"
        i = 1
        for coin in coins:
            print "%d| %.2f %s @ %f฿" % (i, coin.amount, coin.symbol, coin.price)
            i += 1
    elif n == 0:

        totalbtc = 0
        print "Portfolio"
        ticker = polo.returnTicker()

        for coin in coins:
            if coin.symbol != 'BTC':
                currentPrice = float(ticker['BTC_'+coin.symbol]['last'])
                totalbtc += coin.amount * currentPrice
            else:
                totalbtc += coin.amount
                currentPrice = float(ticker['USDT_'+coin.symbol]['last'])
            buyPrice = coin.price
            change = ((currentPrice - buyPrice) / buyPrice) * 100 # calculates precent change
            if coin.symbol != 'BTC':
                print "%.2f %s @ %f฿ has changed %.2f%s" % (coin.amount, coin.symbol, coin.price, change, '%')
            else:
                print "%.4f %s @ $%.2f has changed %.2f%s" % (coin.amount, coin.symbol, coin.price, change, '%')
        
        totalusd = totalbtc * float(ticker['USDT_BTC']['last'])
        print "Total holdings: %.2f฿ or $%.2f" % (totalbtc, totalusd)

class Coin:

    def __init__(self, symbol, amount, price):
        self.symbol = symbol
        self.amount = amount
        self.price = price

#    def addAmount(self, amount):
#        self.amount += amount

if __name__ == "__main__":
    polo = Poloniex()
    coins = []
    
    if os.path.isfile("coins") == False: # checks for an existing coins file
        coin = new()
        pickle.dump(coins, open("coins", "wb"))
    else:
        coins = pickle.load(open("coins", "rb"))
    
    print ''
    menu()
    

