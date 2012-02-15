# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:16:19 2011

@author: Makaye
"""

import os
import glob
import matplotlib.pyplot as plt
from matplotlib import cm as cm
import matplotlib.mlab as mlab

StockDir = 'C:\Users\Makaye\Desktop\Investment\Stocks'
os.chdir(StockDir)
#Exh = 'AMEX'
#os.chdir(Exh)
## find all stocks in the exhcange
#def LoadStocks():
#    StockList = glob.glob('*.csv')
#    StockList = [index.split('.')[0] for index in StockList]
#    AllData = [];
#    for index in StockList:
#        print index
#        CurrentStock = index
#        # read the file
#        fid = open(CurrentStock + '.csv','r')
#        Data = mlab.csv2rec(fid)
#        fid.close()
#        AllData.append(Data)
#        print "AllData appended"    
#    return AllData
#    # Now all the stock data for this exhange is loaded into a list

#def CreateMatrix(AllData,field):
#    N = len(AllData)
#    M = len(AllData[0])
#    StockArray = numpy.zeros([M,N])
#    for i in range(0,N):
#        len(AllData[i].close)
#        StockArray[:,i] = AllData[i].close
#        


def Display(AllData):
    print AllData[0].close
 
def Buy(Stock,StartPoint,Money,TransactionCost):
   # if the stock goes down two days in a row and then 
   # up on the third day 
   # day1 > day2
   # day2 > day3
   # day3 < day4 
   D = Stock.close
   for i in range(len(Stock)-4-StartPoint,3,-1):
       if D[i+3]>D[i+2]>D[i+1]<D[i]:
           SharesToBuy = (Money-TransactionCost)/D[i]
#           result = (range(i,i+4),D[i:i+4],Stock[i:i+4].date,SharesToBuy)
           result = (len(Stock)-i,i,Stock.close[i],SharesToBuy)
           return result
       #day2flag = Stock.close[i-3]>Stock.close[i-2]
       #day3flag = Stock.close[i-2]>Stock.close[i-1]
       #day4flag = Stock.close[i-1]<Stock.close[i]
       #if day2flag & day3flag & day4flag:
           #print Stock.date[i],'BUY'
       #    SharesToBuy = (Money-TransactionCost)/Stock.close[i]
       #    result = (len(Stock)-i,Stock.close[i],SharesToBuy)
           #print 'Buy: ',result           
       #    return result

    
    
def Sell(Stock,StartPoint,Shares,TransactionCost):
    # day1<day2
    # day2<day3
    # day3>day4
    D = Stock.close
    for i in range(len(Stock)-4-StartPoint,3,-1):
        if D[i+3]<D[i+2]<D[i+1]>D[i]:
            Money = Shares*Stock.close[i]-TransactionCost
#            result = (range(i,i+4),D[i:i+4],Stock[i:i+4].date,Money)
            result = (len(Stock)-i,i,Stock.close[i],Money)
            return result
#    for i in range(len(Stock)-1-StartPoint,3,-1):
#        day2flag = Stock.close[i-3]<Stock.close[i-2]
#        day3flag = Stock.close[i-2]<Stock.close[i-1]
#        day4flag = Stock.close[i-1]>Stock.close[i]
#        if day2flag & day3flag & day4flag:
#            #print Stock.date[i],'SELL'
#            Money = Shares*Stock.close[i]-TransactionCost
#            result = (len(Stock)-i,Stock.close[i],Money)
#            return result


        
def BuySell(Stock,Money,TransactionCost):
    StartPoint = 0;    
    BuyPoints = []
    SellPoints = []
    while StartPoint < len(Stock)-100:
        BuyResult = Buy(Stock,StartPoint,Money,TransactionCost)
        BuyPoints.append(BuyResult[1])
        #print 'Buy: ',BuyResult        
        StartPoint = BuyResult[0]
        Shares = BuyResult[3]
        SellResult = Sell(Stock,StartPoint,Shares,TransactionCost)
        SellPoints.append(SellResult[1])
        Money = SellResult[3]
        StartPoint = SellResult[0]
        print 'Sell: ',SellResult
    output=(BuyPoints,SellPoints)
    return output

def PlotData(Stock,buyselldata):
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    
    textsize = 9
    left, width = 0.1, 0.8
    rect1 = [left, 0.1, width, 0.9]

    fig = plt.figure(facecolor='white')
    axescolor  = '#f6f6f6'  # the axies background color

    ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height

    ### plot the relative strength indicator
    prices = Stock.close
   
    fillcolor = 'darkgoldenrod'
    
    plt.plot(Stock.date, prices, color=fillcolor)            
    for i in buyselldata[0]:
        plt.plot(Stock.date[i],prices[i],'bo')
    for i in buyselldata[1]:
        plt.plot(Stock.date[i],prices[i],'rx')
    plt.show()            
            