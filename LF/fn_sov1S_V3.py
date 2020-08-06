
from event_V2 import *
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *
import logging
import threading
import gc

logger = logging.getLogger("main.log")

__all__ = ['Fn_Sov1S']


class Fn_Sov1S(Eventmanager):

    def __init__(self,com,df,idxNo,filename):
        self._idxNo =idxNo
        self.filename = filename
        # self.gen = com
        self.df = df
        self.devicename = df.iloc[self._idxNo, 0]
        self.setup()
        self._opencmdvalue = False
        self._openFBvalue = False
        self._closeFBvalue = False
        self.initilizedigitalinput()
        self.mylock = threading.Lock()
        super().__init__(lambda: self.sov1sprocess())


    def setup(self):
        try:


            for tag,col in self.readalltags():

                if col==3:
                    self.areatag = str(tag)

                if col == 4:
                    self.cmdtag = str(tag)

                if col == 5:
                    self.openFBtag = str(tag)

                if col == 6:
                    self.closeFBtag = str(tag)




        except Exception as e:
            level = logging.ERROR
            messege = "FN_SOV1S" + self.devicename + " Error messege(setup)" + str(e.args)
            logger.log(level, messege)
            log_exception(e)



    def initilizedigitalinput(self):

        client = Communication()
        sta_con_plc = client.opc_client_connect(self.filename)
        readgeneral = ReadGeneral(sta_con_plc)
        writegeneral = WriteGeneral(sta_con_plc)
        if len(self.closeFBtag) > 3:
            writegeneral.writesymbolvalue(self.closeFBtag, 0, 'S7WLBit')


        sta_con_plc.disconnect()


    def sov1sprocess(self):
        try:

            client = Communication()
            sta_con_plc = client.opc_client_connect(self.filename)
            readgeneral = ReadGeneral(sta_con_plc)
            writegeneral = WriteGeneral(sta_con_plc)

            self.cmdtagvalue = readgeneral.readsymbolvalue(self.cmdtag,'S7WLBit','PA')
            if self.cmdtagvalue:
                if len(self.closeFBtag) > 3:
                    writegeneral.writesymbolvalue(self.closeFBtag, 0, 'S7WLBit')
                writegeneral.writesymbolvalue(self.openFBtag, 1, 'S7WLBit')



            if not self.cmdtagvalue:
                writegeneral.writesymbolvalue(self.openFBtag, 0, 'S7WLBit')
                if len(self.closeFBtag) > 3:
                    writegeneral.writesymbolvalue(self.closeFBtag, 1, 'S7WLBit')



                level1 = logging.INFO
                level2 = logging.WARNING
                messege2 = self.devicename + ":" + self.cmdtag + " value is 1"
                messege1 = self.devicename + ":" + self.openFBtag + " is trigger by 1"
                logger.log(level2, messege2)
                logger.log(level1, messege1)

            sta_con_plc.disconnect()
            gc.collect()





        except Exception as e:
            log_exception(e)
            level = logging.INFO
            messege = self.devicename + ":" + " Exception rasied(process): " + str(e.args) + str(e)
            logger.log(level, messege)


    @property
    def areaname(self):
        return self.areatag

    @property
    def OpenCmd(self):
        return self._opencmdvalue


    @OpenCmd.setter
    def OpenCmd(self,value):
        if value != self._opencmdvalue:
            super().fire()
            self._opencmdvalue = value


    def readalltags(self):
        n = 3 
        row, col = self.df.shape
        print(col)
        while n < col:
            data = self.df.iloc[self._idxNo, n]
            yield data,n
            n = n + 1








