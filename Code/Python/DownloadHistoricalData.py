# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 20:50:33 2011

@author: Makaye
"""
import os
import ystockquote
StockNameList = 'C:\Users\Makaye\Desktop\Investment\Code\yahoo_stock_symbols_4.csv'
StockNameWithExchange = 'C:\Users\Makaye\Desktop\Investment\Code\TickersNamesExhanges_4.csv'
fid = open(StockNameList,'r')


Data = fid.readlines()
StockTicker = [day.split(',')[0] for day in Data]
StockName = [day.split(',')[1].split('\n')[0] for day in Data]
fid.close()

StockExh = [ystockquote.get_stock_exchange(tick) for tick in StockTicker]

fid = open(StockNameWithExchange,'w')

for i in range(0,len(StockTicker)):
    temp = StockTicker[i]+','+StockName[i]+','+StockExh[i]+'\n'
    fid.write(temp)
fid.close()
# Create the directories if needed
BaseDir =  'C:\Users\Makaye\Desktop\Investment\Stocks'   
start_date = '20100101'
end_date = '201101023'
for i in range(0,len(StockTicker)):
    CurExh = StockExh[i]   
    CurTick = StockTicker[i]
    CurDir= os.path.join(BaseDir,CurExh)
    if not os.path.exists(CurDir):
        os.makedirs(CurDir)
    # download the data for each exchange
    OutDir = os.path.join(BaseDir,CurExh,CurTick+".csv")
    fid = open(OutDir,'w')
    ys=ystockquote.get_historical_prices(StockTicker[i],start_date,end_date)
    
    for j in ys:
        temp=",".join(["%s"% el for el in j])+'\n'  
        fid.write(temp)
    fid.close()
    
    
    