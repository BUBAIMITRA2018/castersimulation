from  fn_TundishCar2 import  *
from  fn_TundishCar1 import  *
from  fn_CropBucket import  *
import logging


logger = logging.getLogger("main.log")


class Cal_AllTurdishCar:

    def __init__(self,filename):
        self.filename = filename



    def setup(self):
        try:

            self.TurdishCar_1 =  Fn_TundishCar1(self.filename)
            self.TurdishCar_2 = Fn_TundishCar2(self.filename)
            self.CropBucket   = Fn_CropBucket(self.filename)


        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "callallTurdishcar" + str(e.args)
            logger.log(level, messege)





    @property
    def turndishcar1(self):
        return self.TurdishCar_1

    @property
    def turndishcar2(self):
        return self.TurdishCar_2

    @property
    def cropbucket(self):
        return self.CropBucket


