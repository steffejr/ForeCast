# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 20:55:08 2012

@author: Makaye
"""

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

def Buyv2 (Stock,StartPoint,Money,TransactionCost):
    BuyAlgo = [];
    BuyAlgo.append([-1,1])
    for i in range(StartPoint,0,-1):
        SharesToBuy = (Money-TransactionCost)/Stock[i-4]
        if (Stock[i-3]<Stock[i-4])&(Stock[i-3]>Stock[i-2]>Stock[i-1])&(SharesToBuy*(Stock[i-4]-Stock[i-1])>TransactionCost):
                 
#           result = (range(i,i+4),D[i:i+4],Stock[i:i+4].date,SharesToBuy)
           result = (i-4,Stock[i-4],SharesToBuy)
           #print str(i-4)+" Sell: "+str(SharesToBuy)+" at "+str(Stock[i-4])
           return result

def Sellv2(Stock,StartPoint,Shares,TransactionCost):
    # day1(i)<day2(i+1)
    # day2(i+1)<day3(i+2)
    # day3(i+2)>day4(i+3)
    for i in range(StartPoint,0,-1):
        if (Stock[i-4]<Stock[i-3])&(Stock[i-1]<Stock[i-2]<Stock[i-3]):
            Money = Shares*Stock[i-4]-TransactionCost
#            result = (range(i,i+4),D[i:i+4],Stock[i:i+4].date,Money)
            result = (i-4,Stock[i-4],Money)
            return result
               
def BuySell(Stock,StartMoney,TransactionCost):
    StartPoint = len(Stock);    
    BuyPoints = []
    SellPoints = []
    TotalTransactionCosts = 0;
    Money = StartMoney
    while StartPoint > 10:
        try:
            BuyResult = Buyv2(Stock,StartPoint,Money,TransactionCost)
            TotalTransactionCosts = TotalTransactionCosts + TransactionCost
            BuyPoints.append(BuyResult[0])
            #print 'Buy: ',BuyResult        
            StartPoint = BuyResult[0]
            Shares = BuyResult[2]
            SellResult = Sellv2(Stock,StartPoint,Shares,TransactionCost)
            SellPoints.append(SellResult[0])
            TotalTransactionCosts = TotalTransactionCosts + TransactionCost        
            Money = SellResult[2]
            StartPoint = SellResult[0]
           # print 'Buy: ',BuyResult
           # print 'Sell: ',SellResult
        except:
            break
    Return = Money - StartMoney    
    EstReturnRate = Return/(len(Stock)*7/5)
    output=(BuyPoints,SellPoints,Return,TotalTransactionCosts,EstReturnRate)
    return output
    
#def CalculateEarnings(Stock,output):
def FindMaxGain(AllStocks):
    NStocks = AllStocks.shape[1]
    MaxGain = 0;  
    StockIndex = 0;
    for i in range(0,NStocks,1):
        output=BuySell(AllStocks[:,i],1000,5)
        if output[2]>MaxGain:
            MaxGain = output[2]
            StockIndex = i
    output = (MaxGain,StockIndex)
    return output
    
def PlotData(Stock,buyselldata):
    Stock = Stock[::-1]
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    
    textsize = 9
    left, width = 0.1, 0.8
    rect1 = [left, 0.1, width, 0.9]

    fig = plt.figure(facecolor='white')
    axescolor  = '#f6f6f6'  # the axies background color

    ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height

    ### plot the relative strength indicator
    prices = Stock
   
    fillcolor = 'darkgoldenrod'
    
    plt.plot(prices, color=fillcolor)            
    for i in buyselldata[0]:
        plt.plot(i,prices[i],'bo')
    for i in buyselldata[1]:
        plt.plot(i,prices[i],'rx')
    plt.show()            
            