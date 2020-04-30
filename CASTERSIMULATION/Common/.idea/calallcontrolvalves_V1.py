from logger import *
from fn_controlvalve_V1 import *


setup_logging_to_file("allcontrolvalve.log")


class Cal_AllControlValve:

    def __init__(self,df,com,logger):
        self.df = df
        self.logger = logger
        self.com = com
        self.listofcontrolvalves = []
        self.setup()


    def setup(self):
        try:

            n= 0
            self.listofcontrolvalves.clear()
            while n< len(self.df.index):

                self.df.iloc[n, 0] = Fn_ControlValves(self.com, self.df, n,self.logger)
                self.listofcontrolvalves.append(self.df.iloc[n,0])
                n = n + 1

        except Exception as e :
            print(e.args)
            log_exception(e)


    def process(self):
        n = 0

        while n < len(self.listofcontrolvalves):
            self.listofcontrolvalves[n].process()
            n = n + 1



    @property
    def listofallcontrolvalves(self):
        if len(self.listofcontrolvalves) > 0:
            return self.listofcontrolvalves



