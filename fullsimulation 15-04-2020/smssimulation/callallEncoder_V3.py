from logger import *
from fn_Encoder_V3 import *
import logging
import threading

setup_logging_to_file("allencoder.log")
logger = logging.getLogger("main.log")


class Cal_AllEncoder:
    def __init__(self, df, com):
        self.df = df
        self.com = com
        self.listofencoder = []
        self.listofencodersarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:
            # Make a lis of area
            self.listofencoderarea = list(set(self.df['Sub-Area']))

            # Make a lis of devices
            n = 0
            self.listofencoder.clear()
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_Encoder(self.com, self.df, n)
                self.listofencoder.append(self.df.iloc[n, 0])
                n = n + 1

            # per area wise device list
            # Declear empty list
            for area in self.listofencoderarea:
                list1 = []
                for item in self.listofencoder:

                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofencoderarea
            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys, values))



        except Exception as e:
            log_exception(e)
            print("Error messege is:",e.args)
            level = logging.ERROR
            messege = 'Event:' + "callallencoder" + str(e.args)
            logger.log(level, messege)

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['mylock']
        return state

    def __setstate__(self, state):
        # Restore instance attributes.
        self.__dict__.update(state)

    @property
    def listofallencoder(self):
        if len(self.listofencoder) > 0:
            return self.listofencoder


    @property
    def listofencoderareas(self):
        return self.listofencoderarea

    @property
    def getencoderdictionary(self):
        return self.dictionary