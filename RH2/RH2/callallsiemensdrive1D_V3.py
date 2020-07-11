from logger import *
from  fn_Siemens_drive_V3 import *
import logging
import threading



logger = logging.getLogger("main.log")


class Cal_AllSiemensDrive1D:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.com = com
        self.filename = filename
        self.listofsiemensdrive1D = []
        self.listofsiemensdrivearea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:

            # Make a lis of area
            self.listofsiemensdrivearea = list(set(self.df['Sub-Area']))



            # Make a list of devices

            n =0
            self.listofsiemensdrive1D.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_Siemens_Drive(self.com, self.df, n,self.filename)
                self.listofsiemensdrive1D.append(self.df.iloc[n,0])
                n = n + 1

            print(self.listofsiemensdrive1D)




            # per area wise device list
            # Declear empty list
            for area in self.listofsiemensdrivearea:
                list1 = []
                for item in self.listofsiemensdrive1D:

                    if str(item.areaname) == str(area):
                        list1.append(item)

                self.devicelistperarea.append(list1)

            keys = self.listofsiemensdrivearea

            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys,values))



        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "Cal_AllSiemensDrive1D" + str(e.args)
            logger.log(level, messege)



    @property
    def listofdrive1Dir(self):
        return self.listofsiemensdrive1D

    @property
    def listofdriveareas(self):
        return self.listofsiemensdrivearea


    @property
    def getmotordictionary(self):
        return self.dictionary


