from logger import *
import threading
from fn_Cylinder import *
import logging

logger = logging.getLogger("main.log")


class Cal_AllCylinder:

    def __init__(self,df,com,filename):
        self.mylock = threading.Lock()
        self.df = df
        self.filename = filename
        self.com = com
        self.logger = logger
        self.listofcylinder = []
        self.listofcylinderarea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:

            # Make a lis of area
            self.listofcylinderarea = list(set(self.df['Sub-Area']))




            # Make a lis of devices
            n= 0
            self.listofcylinder.clear()


            while n< len(self.df.index):
                self.df.iloc[n, 0] = Fn_Cylinder( self.df, n,self.filename)

                self.listofcylinder.append(self.df.iloc[n,0])
                n = n + 1


            for area in self.listofcylinderarea:
                list1 = []
                for item in self.listofcylinder:
                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofcylinderarea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys,values))



        except Exception as e :
            log_exception(e)

            level = logging.ERROR
            messege = 'Event:' + "callallsov1s" + str(e.args)
            logger.log(level, messege)






    @property
    def listofallcylinder(self):
        return self.listofcylinder

    @property
    def listofcylinderareas(self):
        return self.listofcylinderarea

    @property
    def getcylinderdictionary(self):
        return self.dictionary




