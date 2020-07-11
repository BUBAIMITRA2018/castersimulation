
from callallturndishcar import *


logger = logging.getLogger("main.log")



class allturdishcarprocess:
    def __init__(self,filename):
        self.filename = filename
        self.allturdishcar = Cal_AllTurdishCar(self.filename)


    def process(self):
        self.allturdishcar.turndishcar1.process()
        self.allturdishcar.turndishcar2.process()
        self.allturdishcar.cropbucket.process()

















