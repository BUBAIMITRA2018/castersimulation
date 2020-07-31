from logger import *
import gc
from  fn_motor1D_V4 import *
import logging
import threading

logger = logging.getLogger("main.log")


class Cal_AllMotor1D:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.com = com
        self.filename = filename
        self.listofmotor1D = []
        self.listofmotorarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
            # print("dictionary is executed ", self.dictionary)

            # Make a lis of area
            self.listofmotorarea = list(set(self.df['Sub-Area']))

            # Make a list of devices

            n =0
            self.listofmotor1D.clear()
            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_Motor1D(self.com, self.df, n,self.filename)
                self.listofmotor1D.append(self.df.iloc[n,0])
                n = n + 1



            # per area wise device list
            # Declear empty list
            for area in self.listofmotorarea:
                list1 = []
                for item in self.listofmotor1D:

                    if str(item.areaname) == str(area):
                        list1.append(item)

                self.devicelistperarea.append(list1)

            keys = self.listofmotorarea

            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys,values))







        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallmotor1D" + str(e.args)
            logger.log(level, messege)




    @property
    def listofmotor1Dir(self):
        return self.listofmotor1D

    @property
    def listofmotorareas(self):
        return self.listofmotorarea


    @property
    def getmotordictionary(self):
        return self.dictionary


