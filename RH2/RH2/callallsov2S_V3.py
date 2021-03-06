from logger import *
from fn_sov2S_V3 import *
from clientcomm_v1 import *



logger = logging.getLogger("main.log")


class Cal_AllSov2S:
    def __init__(self, df, com,filename):
        self.df = df
        self.com = com
        self.filename = filename
        self.listofsov2s = []
        self.listofsov2sarea = []
        self.devicelistperarea = [[]]
        self.setup()

    def setup(self):
        try:

            # Make a lis of area
            self.listofsov2sarea = list(set(self.df['Sub-Area']))

            # Make a lis of devices

            n = 0
            self.listofsov2s.clear()
            while n < len(self.df.index):
                self.df.iloc[n, 0] = Fn_Sov2S(self.com, self.df, n,self.filename)
                self.listofsov2s.append(self.df.iloc[n, 0])
                n = n + 1

            # per area wise device list
            # Declear empty list
            for area in self.listofsov2sarea:
                list1 = []
                for item in self.listofsov2s:

                    if str(item.areaname) == str(area):
                        list1.append(item)
                self.devicelistperarea.append(list1)

            keys = self.listofsov2sarea
            values = self.devicelistperarea[1:]

            # Declear empty list
            self.dictionary = dict(zip(keys, values))




        except Exception as e:
            log_exception(e)
            print("Error messege is:",e.args)
            level = logging.ERROR
            messege = 'Event:' + "callallsov2s" + str(e.args)
            logger.log(level, messege)



    @property
    def listofallsov2s(self):
        if len(self.listofsov2s) > 0:
            return self.listofsov2s


    @property
    def listofsov2sareas(self):
        return self.listofsov2sarea

    @property
    def getmotordictionary(self):
        return self.dictionary