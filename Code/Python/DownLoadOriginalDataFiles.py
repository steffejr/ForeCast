# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 19:38:18 2011

@author: Makaye
"""
import ystockquote as ys
import os


def AddStockChangeToTickerList():
    TickerFile = 'C:\Users\Makaye\Desktop\Investment\Code\yahoo_stock_symbols_4.csv'
    OutTickerFile = 'C:\Users\Makaye\Desktop\Investment\Code\TickersNamesExhanges_4.csv'
    fid = open(TickerFile,'r')
#    fidOut = open(OutTickerFile,'w')    
    TickerList = fid.readlines() 
    Data = [];
    count = 0;
    N = len(TickerList)
    for i in TickerList:
        count = count + 1
        print str(count) + ':' + str(N)
        i = i.partition('\n')[0]
        i = i.split(',')
        Exh = ys.get_stock_exchange(i[0])        
        Data.append([i[0],i[1],Exh])
    fid.close()
    return Data
    WriteToFile(OutTickerFile,Data)
    
    
def HelloWorld(Name):
    print "Hello: " + Name   
    GoodBye(Name)
    
def GoodBye(Name):
    print "Goodby: " + Name    
    
def WriteToFile(FileName,Data):
    fid = open(FileName,'w')
    for i in Data:
        for j in i:
            fid.write(j)
            fid.write(',')
        fid.write('\n')
    fid.close()

def DownLoadStocks():
    #StockNameList = 'C:\Users\Makaye\Desktop\Investment\Code\yahoo_stock_symbols_4.csv'
    StockNameWithExchange = 'C:\Users\Makaye\Desktop\Investment\Code\TickersNamesExhanges_4.csv'
    fid = open(StockNameWithExchange,'r')
    Data = fid.readlines()
    StockTicker = [day.split(',')[0] for day in Data]
    #StockName = [day.split(',')[1].split('\n')[0] for day in Data]
    StockExchange = [day.split(',')[2].split('\n')[0] for day in Data]
    fid.close()
    
    # Create the directories if needed
    BaseDir =  'C:\Users\Makaye\Desktop\Investment\Stocks'   
    start_date = '20100101'
    end_date = '20111111'
    for i in range(0,len(StockTicker)):
        CurExh = StockExchange[i]   
        CurTick = StockTicker[i]
        CurDir= os.path.join(BaseDir,CurExh)
        if not os.path.exists(CurDir):
            os.makedirs(CurDir)
        # download the data for each exchange
        OutDir = os.path.join(BaseDir,CurExh,CurTick+".csv")
        if not os.path.exists(OutDir):
            try:
                print "DownLoading: "+CurExh+": "+CurTick+", "+str(i)+"/"+str(len(StockTicker)) 
                fid = open(OutDir,'w')
                Y=ys.get_historical_prices(StockTicker[i],start_date,end_date)
                
                for j in Y:
                    
                    temp=",".join(["%s"% el for el in j])+'\n'  
                    fid.write(temp)
                fid.close()
            except:
                print "Problem with: "+CurExh+": "+CurTick
        