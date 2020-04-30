clifrom logger import *
from fn_analogTx import *


setup_logging_to_file("allanalog.log")


class Cal_AllAnalogInputs:

    def __init__(self,df,com):
        self.df = df
        self.com = com
        self.listofanalogs = []


    def setup(self,elementlist):
        try:

            n= 0
            self.listofanalogs.clear()
            while n< len(self.df.index):

                self.df.iloc[n, 0] = Fn_AnalogTx(self.com, self.df, n)
                self.listofanalogs.append(self.df.iloc[n,0])
                n = n + 1




        except Exception as e :
            print(e.args)
            log_exception(e)

    @property
    def listofallsov1s(self):
        if len(self.listofanalogs) > 0:
            return self.listofanalogs



