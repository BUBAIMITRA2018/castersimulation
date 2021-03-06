from logger import *
from fn_ABP_drive_V3 import *
import logging

logger = logging.getLogger("main.log")
setup_logging_to_file("alldrives.log")


class Cal_ABBDrives:

    def __init__(self,df,com):
        self.df = df
        self.com = com
        self.listofdrives = []
        self.listofdrivearea = []
        self.devicelistperarea = [[]]
        self.setup()


    def setup(self):
        try:
            self.listofdrivearea = list(set(self.df['Sub-Area']))

            n= 0
            self.listofdrives.clear()
            while n< len(self.df.index):

                self.df.iloc[n, 0] = Fn_ABP_Drive(self.com, self.df, n)
                self.listofdrives.append(self.df.iloc[n,0])
                n = n + 1



            # per area wise device list
            # Declear empty list
            for area in self.listofdrivearea:
                list1 = []
                for item in self.listofdrives:
                    if item.areaname == area:
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofdrivearea
            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys, values))
            print(self.dictionary)

        except Exception as e :
            level = logging.ERROR
            messege = 'Event:' + "callalldrives" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    def __setstate__(self, state):
        # Restore instance attributes.
        self.__dict__.update(state)


    @property
    def listofalldrives(self):
        if len(self.listofalldrives) > 0:
            return self.listofalldrives

    @property
    def listofdriveareas(self):
        return self.listofdrivearea

    @property
    def getmotordictionary(self):
        return self.dictionary
