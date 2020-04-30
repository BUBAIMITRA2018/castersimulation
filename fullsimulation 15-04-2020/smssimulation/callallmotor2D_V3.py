from logger import *
from fn_motor2D_V3 import *
import logging
import threading

setup_logging_to_file("allmotor2D.log")
logger = logging.getLogger("main.log")

class Cal_AllMotor2D:
    def __init__(self, df, com,filename):
        self.df = df
        self.com = com
        self.filename = filename
        self.listofmotor2D = []
        self.listofmotorarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
            # Make a lis of area
            self.listofmotorarea = list(set(self.df['Sub-Area']))


            # Make a lis of devices

            self.listofmotor2D.clear()
            n = 0
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_Motor2D(self.com, self.df, n,self.filename)
                self.listofmotor2D.append(self.df.iloc[n, 0])
                n = n + 1
            # per area wise device list
            # Declear empty list
            for area in self.listofmotorarea:
                list1 = []
                for item in self.listofmotor2D:

                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofmotorarea
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
        if len(self.listofmotor2D)>0:
            return self.listofmotor2D

    @property
    def listofmotorareas(self):
        return self.listofmotorarea


    @property
    def getmotordictionary(self):
        return self.dictionary


