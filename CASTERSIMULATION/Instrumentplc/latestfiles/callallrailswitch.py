from logger import *
from fn_railswitch import *
import logging
import threading


logger = logging.getLogger("main.log")

class Cal_AllRailSwitch:
    def __init__(self, df, com,filename):
        self.df = df
        self.com = com
        self.filename = filename
        self.listofrailswitch = []
        self.listofrailswitcharea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
            # Make a lis of area
            self.listofrailswitcharea = list(set(self.df['Sub-Area']))


            # Make a lis of devices

            self.listofrailswitch.clear()
            n = 0
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_RailSwitch(self.com, self.df, n,self.filename)
                self.listofrailswitch.append(self.df.iloc[n, 0])
                n = n + 1
            # per area wise device list
            # Declear empty list
            for area in self.listofrailswitcharea:
                list1 = []
                for item in self.listofrailswitch:

                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofrailswitcharea
            values = self.devicelistperarea[1:]
            # Declear empty list
            self.dictionary = dict(zip(keys,values))



        except Exception as e:
            log_exception(e)
            level = logging.ERROR
            messege = 'Event:' + "callallmotor2D" + str(e.args)
            logger.log(level, messege)






    @property
    def listofallrailswitch(self):
        if len(self.listofrailswitch)>0:
            return self.listofrailswitch

    @property
    def listofrailswitchareas(self):
        return self.listofrailswitcharea


    @property
    def getrailswitchdictionary(self):
        return self.dictionary