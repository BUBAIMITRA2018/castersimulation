from logger import *
from fn_conveyor2D_V3 import *
import logging

logger = logging.getLogger("main.log")

class Cal_AllMotor2D:
    def __init__(self, df, com,filename):
        self.df = df
        self.com = com
        self.filename = filename
        self.listofconveyor2D = []
        self.listofconveyorarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
            # Make a lis of area
            self.listofconveyorarea = list(set(self.df['Sub-Area']))


            # Make a lis of devices

            self.listofconveyor2D.clear()
            n = 0
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_Conveyor2D(self.com, self.df, n,self.filename)
                self.listofconveyor2D.append(self.df.iloc[n, 0])
                n = n + 1
            # per area wise device list
            # Declear empty list
            for area in self.listofconveyorarea:
                list1 = []
                for item in self.listofconveyor2D:

                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofconveyorarea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys,values))



        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallmotor2D" + str(e.args)
            logger.log(level, messege)






    @property
    def listofallmotor2D(self):
        if len(self.listofconveyor2D)>0:
            return self.listofconveyor2D

    @property
    def listofmotorareas(self):
        return self.listofconveyorarea


    @property
    def getconveyordictionary(self):
        return self.dictionary


