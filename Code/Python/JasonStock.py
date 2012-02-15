'''
ToDO: Update the load Close/High ... etc tyo be just like the load openv2
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
import ystockquote
import matplotlib.pyplot as plt
from matplotlib import cm as cm
import matplotlib.mlab as mlab
import numpy
import datetime
import scipy.io as sio

class JasonStock():
    StockDir = 'C:\Users\Makaye\Desktop\Investment\Stocks'
    os.chdir(StockDir)
    Exh = 'NYSE'
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
        #self.CreateDateArray(100)
        #self.CreateTotalDataArray(100)
        
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
        LatestDate = self.AllData[0][0].date
        for i in range(0,len(self.AllData),1):
            print LatestDate
            CurrentLatestDate = self.AllData[i][0].date
            print str(i) +' ' +str(CurrentLatestDate) +' '+str(LatestDate)
            if CurrentLatestDate > LatestDate:
                print "TRUE"
                LatestDate = CurrentLatestDate
            print self.StockList[i]+' '+str(CurrentLatestDate)
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
        fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'r')
        CurrentData = fid.readline()
        CurrentData = fid.readline()
        LatestDate = CurrentData.split(',')[0]
#        LatestDate = self.AllData[Index].date[0]
        year=LatestDate.split('-')[0]
        mon=LatestDate.split('-')[1]
        day=LatestDate.split('-')[2]
        #year=str(LatestDate.year)    
        #mon=str(LatestDate.month).zfill(2)
        #day=str(LatestDate.day).zfill(2)
        LatestDate = year+mon+day        
        
        # Check to see if this stock needs to even be updated
        if self.Today == LatestDate:
            print "up to date"
        else:
        # read the current data
        # do not include the first line
            ys=ystockquote.get_historical_prices(StockTicker,LatestDate,self.Today)
            #print ys
            # Check to see if the returned infor has an error or not
            if str(ys).find('doctype') == -1:  
                #fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'r')
                # rewind the file                
                fid.seek(0)                
                CurrentData = fid.readline()
                #print CurrentData
                CurrentData = fid.readlines()
                fid.close()
                fid = open(os.path.join(self.StockDir,self.Exh,StockTicker+'.csv'),'w')
                
                for j in ys:
                    temp=",".join(["%s"% el for el in j])+'\n'  
                    fid.write(temp)
                
                fid.writelines(CurrentData)            
                fid.close()
            else:
                print "Problem retrieving data"
        
    def PrintExh(self):
        print self.Exh
    
    def GetStockList(self):
        StockList = glob.glob('*.csv')
        StockList = [index.split('.')[0] for index in StockList]
        self.StockList = StockList
        
    def LoadStockList(self, StockList):
        for i in StockList:
            self.LoadOneStock(i)
            
    def LoadOneStock(self,StockTicker):
        # Load data from one stock and save the data into the AllData array
        Data=self.LoadStock(StockTicker)   
        self.AllData.append(Data)
        self.NStocks = len(self.AllData)
        
    def LoadStock(self,StockTicker):
        # Load data for one stoick from a CSV file
        if self.CheckStockInList(StockTicker):
            CurrentStock = StockTicker
            # read the file
            tic = time.clock()
            fid = open(CurrentStock + '.csv','r')
            Data = mlab.csv2rec(fid)
            fid.close()
            toc=time.clock()
            ElapsedTime = toc - tic
            print "\t"+CurrentStock+"\tIt took "+str(ElapsedTime)+" s to load" 
            return Data
            
        else:
            print 'The ticker: ' + StockTicker+' is not in the current list.'
    
    def LoadAllStocks(self):
        print "Loading Stocks"
        for index in self.StockList:
            Data=self.LoadStock(index)      
            self.AllData.append(Data)
            #print "AllData appended"    
        self.NStocks = len(self.AllData)

    def CreateDateArray(self,NDays):
        # Findthe data that has the latest date as the first value
        # otherwise skip to the next stock
        index = 0;
        while index < self.NStocks:
            if self.AllData[index][0].date == self.LatestDate:
                self.Dates = self.AllData[index].date[0:NDays]
                break
            else:
                index = index + 1
     
    def CreateOpenArray(self,NDays):
        # find the latest day of the current stock
        # The aim of this ( I think) is to check the start dates 
        # of all the stocks and if one is not up to date then a zero is used.
        OpenData = numpy.zeros([NDays,self.NStocks])
        for index in range(0,self.NStocks,1):
            for i in range(0,NDays,1):
                if self.Dates[i]==self.AllData[index][0].date:
                    break
            OpenData[i:NDays,index] = self.AllData[index].open[0:NDays-i]
        self.OpenData = OpenData

    def CreateCloseArray(self,NDays):
        CloseData = numpy.zeros([NDays,self.NStocks])
        for index in range(0,self.NStocks,1):
            for i in range(0,NDays,1):
                if self.Dates[i]==self.AllData[index][0].date:
                    break
            CloseData[i:NDays,index] = self.AllData[index].close[0:NDays-i]
        self.CloseData = CloseData
        
    def CreateHighArray(self,NDays):
        HighData = numpy.zeros([NDays,self.NStocks])
        for index in range(0,self.NStocks,1):
            for i in range(0,NDays,1):
                if self.Dates[i]==self.AllData[index][0].date:
                    break
            HighData[i:NDays,index] = self.AllData[index].high[0:NDays-i]
        self.HighData = HighData
        
    def CreateLowArray(self,NDays):
        LowData = numpy.zeros([NDays,self.NStocks])
        for index in range(0,self.NStocks,1):
            for i in range(0,NDays,1):
                if self.Dates[i]==self.AllData[index][0].date:
                    break
            LowData[i:NDays,index] = self.AllData[index].low[0:NDays-i]
        self.LowData = LowData
    
    def CreateVolumeArray(self,NDays):
        VolumeData = numpy.zeros([NDays,self.NStocks])
        for index in range(0,self.NStocks,1):
            for i in range(0,NDays,1):
                if self.Dates[i]==self.AllData[index][0].date:
                    break
            VolumeData[i:NDays,index] = self.AllData[index].volume[0:NDays-i]
        self.VolumeData = VolumeData

    def CreateTotalDataArray(self,NDays):
        self.PrintMostRecentDate()
        self.CreateDateArray(NDays)
        self.CreateOpenArray(NDays)
        self.CreateCloseArray(NDays)
        self.CreateLowArray(NDays)
        self.CreateHighArray(NDays)
        self.CreateVolumeArray(NDays)
        TotalData = numpy.zeros([NDays,self.NStocks,5])
        TotalData[:,:,0] = self.OpenData
        TotalData[:,:,1] = self.LowData
        TotalData[:,:,2] = self.HighData
        TotalData[:,:,3] = self.CloseData
        TotalData[:,:,4] = self.VolumeData
        self.TotalData = TotalData

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

        


#JS.PlotData(JS.TotalData[:,0,1])
