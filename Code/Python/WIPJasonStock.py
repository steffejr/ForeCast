'''
ToDo: I updated the CreateOpen but it needs to work even when there is not enough data in the file
Update the other CreatXXX functions also.
Done: Make the load data operation faster. Right now I load data from the text 
files then create the data arrays. It may be better to just create the data
arrays directly without first loading the data. What I have
works but takes a few minutes. Maybe open each file and read XX number of lines
Done: Update the load Close/High ... etc tyo be just like the load openv2
Done: For the update stocks have it take a single StockName. Check to make sure that this 
ticker is in StockList.
If so find the latest date for THIS stock. Then update the file.
So the procedure is to load all data.
Then update all files and reload the data.
Maybe the program should update when it loads the data up??
'''
import os
import time
import glob
import datetime
import ystockquote as ys
import matplotlib.pyplot as plt
from matplotlib import cm as cm
import matplotlib.mlab as mlab
import numpy
import datetime
import scipy.io as sio
import csv

class JasonStock():
    StockDir = 'C:\Users\Makaye\Desktop\Investment\Stocks'
    os.chdir(StockDir)
    Exh = 'AMEX'
    EarliestDate = '20100101' # use this for when the file needs to be re downloaded
    AllData = []
    os.chdir(Exh)
    def __init__(self):
        self.PrintExh()
        self.GetStockList()
        #self.LoadStocks()
        #self.PrintMostRecentDate()
        #self.CreateTotalDataArray(20)
        self.GetToday()
        print "Today is:" + self.Today
        self.LoadAllStocks()
        self.PrintMostRecentDate()
        #self.CreateDateArray(400)
        #self.CreateOpenArray()
        #self.CreateDateArray(100)
        self.CreateTotalDataArray(400)
        
    def CheckStockInList(self,StockTicker):
        flag = False
        for i in self.StockList:
            if StockTicker.upper() == i.upper():
                flag = True
                break
        return flag
        
    def ClearAllData(self):
        self.AllData = []
        self.NStocks = 0
        
    def FindExchanges(self):
        ExhList = os.listdir(self.StockDir)
        self.ExhList = ExhList
        print ExhList
    
    def PrintMostRecentDate(self):
        print "Most recent dates are:"
        LatestDate = datetime.date.min
        for i in range(0,len(self.AllData),1):
            if len(self.AllData[i]):
        #        print LatestDate
                CurrentLatestDate = self.AllData[i][0][0]
        #        print str(i) +' ' +str(CurrentLatestDate) +' '+str(LatestDate)
                if CurrentLatestDate > LatestDate:  
         #           print "TRUE"
                    LatestDate = CurrentLatestDate
         #           print self.StockList[i]+' '+str(CurrentLatestDate)
        self.LatestDate = LatestDate    

    def GetToday(self):
        d = datetime.date.today()
        year=str(d.year)    
        mon=str(d.month).zfill(2)
        day=str(d.day).zfill(2)
        Today = year+mon+day
        self.Today = Today


    def UpDateOneStock(self,StockTicker):
        if self.CheckStockInList(StockTicker):
            self.UpDateStockData(StockTicker)
        else:
            print 'The ticker: ' + StockTicker+' is not in the current list.'

    def UpDateStockList(self, StockList):
        for i in StockList:
            self.UpDateOneStock(i)
        
    def UpDateAllStocks(self):
        for i in self.StockList:
            self.UpDateStockData(i)
            
    def UpDateStockData(self,StockTicker):
        # open the file
        # find the last date in the stock
                
        #Index = self.StockList.index(StockTicker)
        print "Updating: "+StockTicker
        # Check for the latest date in the file
        # open the file        
        fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'r')
        # read the first line of the file        
        CurrentData = fid.readline()
        #print CurrentData
        # check to see if there is garbage in the file
        # no garbage
        if (CurrentData.find('doctype') == -1) & len(CurrentData)>0:
            CurrentData = fid.readline()
            LatestDate = CurrentData.split(',')[0]
            year=LatestDate.split('-')[0]
            mon=LatestDate.split('-')[1]
            day=LatestDate.split('-')[2]
            LatestDate = year+mon+day        
        # Check to see if this stock needs to even be updated
            if self.Today == LatestDate:
                print "up to date"
            else:
        # read the current data
        # do not include the first line
                Y=ys.get_historical_prices(StockTicker,LatestDate,self.Today)
            #print ys
            # Check to see if the returned infor has an error or not
                if str(Y).find('doctype') == -1:  
                #fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'r')
                # rewind the file                
                    fid.seek(0)       
                    # read the first line which is the header line
                    CurrentData = fid.readline()
                    # overwrite the header line because it is included in the newer 
                    # data set
                    CurrentData = fid.readlines()
                    # close the file
                    fid.close()
                    # reopen the file with write privaledges
                    fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'w')
                    # write the new data to the file
                    for j in Y:
                        temp=",".join(["%s"% el for el in j])+'\n'  
                        fid.write(temp)
                    # write the old data to the file
                    fid.writelines(CurrentData)            
                    # close the file
                    fid.close()
                else:
                    print "Problem retrieving data"
        else:
            # There is a problem with this file so download it again "fresh"
            fid.close()
            try:
                print "DownLoading: "+self.CurExh+": "+StockTicker 
                fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'w')
                Y=ys.get_historical_prices(StockTicker,self.EarliestDate,self.Today)
                for j in Y:
                    temp=",".join(["%s"% el for el in j])+'\n'  
                    fid.write(temp)
                fid.close()
            except:
                print "Problem with: "+self.Exh+": "+StockTicker        
        
        
    def PrintExh(self):
        print self.Exh
    
    def GetStockList(self):
        StockList = glob.glob('*.csv')
        StockList = [index.split('.')[0] for index in StockList]
        self.StockList = StockList
        
    def LoadStockList(self, StockList):
        self.ClearAllData()
        for i in StockList:
            self.LoadOneStock(i)
            
    def LoadOneStock(self,StockTicker):
        self.ClearAllData()
        # Load data from one stock and save the data into the AllData array
        Data=self.LoadStockv2(StockTicker)   
        # only append the stock if there is actually data in it
        if len(Data)>0:
            self.AllData.append(Data)
        self.NStocks = len(self.AllData)
            
#    def LoadOneStock(self,StockTicker):
#        # Load data from one stock and save the data into the AllData array
#        Data=self.LoadStockv2(StockTicker)   
#        # only append the stock if there is actually data in it
#        if len(Data)>0:
#            self.AllData.append(Data)
#        self.NStocks = len(self.AllData)
        
#    def LoadStock(self,StockTicker):
#        # Load data for one stoick from a CSV file
#        if self.CheckStockInList(StockTicker):
#            CurrentStock = StockTicker
#            # read the file
#            tic = time.clock()
#            fid = open(CurrentStock + '.csv','r')
#            # check each stock to make sure that the data is good
#            CurrentData = fid.readline()
#            if (CurrentData.find('doctype') == -1) & (len(CurrentData)>0):
#                # rewind the file                
#                fid.seek(0)                
#                Data = mlab.csv2rec(fid)
#                fid.close()
#                toc=time.clock()
#                ElapsedTime = toc - tic
#                print "\t"+CurrentStock+"\tIt took "+str(ElapsedTime)+" s to load" 
#                return Data
#            else:
#                Data=[]
#                fid.close()
#                print "Problem with: "+ StockTicker
#                return Data
#        else:
#            print 'The ticker: ' + StockTicker+' is not in the current list.'

    def LoadStockv2(self,StockTicker):
        #tic = time.clock()
        TempData = csv.reader(open(StockTicker + '.csv','r'))
        Data=[]
        for i in TempData:
            if i[0].find('doctype')>0:
                break
            elif i[0] != 'Date':
                Date = datetime.date(int(i[0][0:4]),int(i[0][5:7]),int(i[0][8:10]))
                Open = float(i[1])
                High = float(i[2])
                Low = float(i[3])            
                Close = float(i[4])
                Volume = float(i[5])
                AdjClose = float(i[6])
                Data.append((Date,Open,High,Low,Close,Volume,AdjClose))
        #toc=time.clock()
        #ElapsedTime = toc - tic
        #print "\t"+StockTicker+"\tIt took "+str(ElapsedTime)+" s to load" 
        #print "\t"+StockTicker
        return Data
        
    def LoadAllStocks(self):
        self.ClearAllData()
        print "Loading Stocks"
        tic = time.clock()
        for index in self.StockList:
            Data=self.LoadStockv2(index)      
            if len(Data)>0:
                self.AllData.append(Data)
            #print "AllData appended"    
        self.NStocks = len(self.AllData)
        toc=time.clock()
        ElapsedTime = toc - tic
        print "\tIt took "+str(ElapsedTime)+" s to load" 
        
    def CreateDateArray(self,NDays):
        # Findthe data that has the latest date as the first value
        # otherwise skip to the next stock
        index = 0;
        flag = True
        while (index < self.NStocks) & flag:
            print index
            if len(self.AllData[index])>0:
                if self.AllData[index][0][0] == self.LatestDate:
                    self.Dates = []                    
                    for i in range(0,NDays,1):
                        self.Dates.append(self.AllData[0][i][0])
                    #self.Dates = self.AllData[index].date[0:NDays]
                    flag = False
                else:
                    index = index + 1
            else:
                index = index + 1

    def CreateDataArray(self,Column):
        NDays = len(self.Dates)
        Data = numpy.zeros([NDays,self.NStocks])
        # cycle over each stock
        for index in range(0,self.NStocks,1):
            # cycle over each day
            # find the latest date. This allows for the data file to NOT have 
            # the most recent date in it
            i = self.Dates.index(self.AllData[index][0][0])
            #print str(index)+':'+str(i)
            NDaysInThisStock=len(self.AllData[index])
            if NDaysInThisStock > NDays:
                LoadLength = NDays-i
            else:
                LoadLength = NDaysInThisStock-i
                
            for j in range(i,LoadLength,1):
                Data[j,index]=self.AllData[index][j][Column]
            #OpenData[i:i+len(self.AllData[index].open[0:NDays-i]),index] = self.AllData[index].open[0:NDays-i]
        return Data
            

    def CreateTotalDataArray(self,NDays):
        self.PrintMostRecentDate()
        
        self.CreateDateArray(NDays)
        self.OpenData=self.CreateDataArray(1)
        self.CloseData=self.CreateDataArray(2)
        self.HighData=self.CreateDataArray(3)
        self.LowData=self.CreateDataArray(4)
        self.VolumeData=self.CreateDataArray(5)
        
#        self.CreateOpenArray(NDays)
#        self.CreateCloseArray(NDays)
#        self.CreateLowArray(NDays)
#        self.CreateHighArray(NDays)
#        self.CreateVolumeArray(NDays)
#        TotalData = numpy.zeros([NDays,self.NStocks,5])
#        TotalData[:,:,0] = self.OpenData
#        TotalData[:,:,1] = self.LowData
#        TotalData[:,:,2] = self.HighData
#        TotalData[:,:,3] = self.CloseData
#        TotalData[:,:,4] = self.VolumeData
#        self.TotalData = TotalData

    def SaveDataToMatLab(self,NDays,StockList):
        # convert the Dates to an array
        DateArray=numpy.zeros(NDays)
        for i in range(0,NDays,1):
            DateArray[i]=int(str(self.Dates[i].month).zfill(2)+str(self.Dates[i].day).zfill(2)+str(self.Dates[i].year).zfill(2))
        index=range(1,NDays+1,1)
        
        now=datetime.datetime.now()
        DateStr = str(now.month).zfill(2)+'_'+str(now.day).zfill(2)+'_'+str(now.year)+'_'+str(now.hour).zfill(2)+str(now.minute).zfill(2)
        FileName = self.Exh+'_'+str(self.NStocks)+'Stocks_'+DateStr+'.mat'
        OutFile=os.path.join(self.StockDir,FileName)
        sio.savemat(OutFile,{'StockList':StockList,'index':index,'dates':DateArray,'close':self.CloseData,'open':self.OpenData,'volume':self.VolumeData,'high':self.HighData,'low':self.LowData})
        

        
    def PlotData(self,Data):
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    
        textsize = 9
        left, width = 0.1, 0.8
        rect1 = [left, 0.1, width, 0.9]

        fig = plt.figure(facecolor='white')
        axescolor  = '#f6f6f6'  # the axies background color

        ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height

        ### plot the relative strength indicator
   
        fillcolor = 'darkgoldenrod'
        plt.plot(self.Dates, Data, color=fillcolor)            

    #for i in buyselldata[0]:
    #    plt.plot(Stock.date[i],prices[i],'bo')
    #for i in buyselldata[1]:
    #    plt.plot(Stock.date[i],prices[i],'rx')
        plt.show()
