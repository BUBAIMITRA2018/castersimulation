import gc
from clientcomm_v1 import *
from  writegeneral_v2 import *
logger = logging.getLogger("main.log")
__all__ = ['Fn_outsignal']


class Fn_outsignal():

    def __init__(self, com, df, idxNo,filename ):
        self._idxNo = idxNo
        self.gen = com
        self.filename = filename
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self.initilizedigitalinput()

    def setup(self):

        try:
            for tag, col in self.readalltags():

                if col == 4:
                    self.OutDigital = str(tag)

                if col == 5:
                    self.Value = int(tag)

            gc.collect()

        except Exception as e:
            level = logging.ERROR
            messege = "FN_OUTSIGNAL" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)

    def initilizedigitalinput(self):
        try:
            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            writegeneral = WriteGeneral(sta_con_plc)
            writegeneral.writesymbolvalue(self.OutDigital, self.Value, 'S7WLBit')
            level = logging.INFO
            messege = "FN_OUTSIGNAL" +self.devicename + ":" + self.OutDigital + str(self.Value)
            logger.log(level, messege)
            sta_con_plc.disconnect()

            gc.collect()

        except Exception as e:
            level = logging.ERROR
            messege = "Fn_Outputsignal" + self.devicename + " Error messege(initilization)" + str(e.args)
            logger.log(level, messege)

    def readalltags(self):
        n = 3
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data, n
            n = n + 1

