# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\Makaye\.spyder2\.temp.py
"""
import glob
import os

#import yss # find on source forge for downloading stock symbols

BaseDirectory = 'C:\Users\Makaye\Desktop\Investment\Stocks'


StockList =glob.glob(os.path.join(BaseDirectory,'NasdaqNM','*.csv'))
NStocks = len(StockList)
# open file
fid = open(StockList[0])

Header = fid.readline()
FirstLine = fid.readline()
# read the entire file
# rewind file
fid.seek(0)
Data = fid.readline()
Data = fid.readlines()
fid.close()
StockOpen=[float(day.split(',')[1]) for day in Data] 
StockHigh=[float(day.split(',')[2]) for day in Data] 
StockLow=[float(day.split(',')[3]) for day in Data] 
StockClose=[float(day.split(',')[4]) for day in Data] 
StockVolume=[float(day.split(',')[5]) for day in Data] 

