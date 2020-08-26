
from callallturndishcar import *


logger = logging.getLogger("main.log")



class allturdishcarprocess:
    def __init__(self,filename):
        self.filename = filename
        self.allturdishcar = Cal_AllTurdishCar(self.filename)


    def process(self):
        try:
            self.allturdishcar.turndishcar1.process()
            self.allturdishcar.turndishcar2.process()
            self.allturdishcar.cropbucket.process()

        except Exception as e:
            level = logging.INFO
            messege = "allturdishcarprocess" + ":" + " Exception rasied: " + str(e.args) + str(e)
            logger.log(level, messege)


















