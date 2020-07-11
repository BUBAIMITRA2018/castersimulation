from logger import *
from fn_controlvalve_V3 import *
import logging
import threading


class Cal_AllControlValves:

    def __init__(self,df,com,filename):
        self.df = df
        self.mylock = threading.Lock()
        self.filename = filename
        self.com = com
        self.listofcontrolvalvesobjects = []
        self.listofcontrolvalvesarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:
            # Make a lis of area
            self.listofcontrolvalvesarea = list(set(self.df['Sub-Area']))
            # Make a list of devices
            n= 0
            self.listofcontrolvalvesobjects.clear()
            while n< len(self.df.index):

                self.df.iloc[n, 0] = Fn_ControlValves(self.com, self.df, n,self.filename)
                self.listofcontrolvalvesobjects.append(self.df.iloc[n,0])
                n = n + 1

            # per area wise device list
            # Declear empty list
                # per area wise device list
                # Declear empty list
            for area in self.listofcontrolvalvesarea:
                list1 = []
                for item in self.listofcontrolvalvesobjects:
                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofcontrolvalvesarea
            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys, values))




        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "callallcontrolvalves" + str(e.args)
            # logger.log(level, messege)
            log_exception(e)



    @property
    def listofanalogs(self):
        if len(self.listofcontrolvalvesobjects) > 0:
            return self.listofcontrolvalvesobjects

    @property
    def listofcontrolvalvesareas(self):
        return self.listofcontrolvalvesarea

    @property
    def getcontrolvalvedictionary(self):
        return self.dictionary

