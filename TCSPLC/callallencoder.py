from  fn_Cylinder import  *
from  fn_Arm2Lift_Encoder import  *
from  fn_BA01_BWL_Turret_Encoder import  *
from  fn_TDCar1LiftLower_Encoder import  *
from fn_TDCar2LiftLower_Encoder import *
from fn_LevellingRollPos_Encoder import *
from fn_DB_Encoder import *
from fn_PR_Encoder import *
from fn_Shear_Angel_Encoder import *
from fn_WSD_Encoder import *

import logging

logger = logging.getLogger("main.log")


class Cal_AllEncoder:

    def __init__(self,filename):
        self.filename = filename
        # self.Arm1Lift_Encoder = None
        # self.Arm2Lift_Encoder = None
        # self.BA01_BWL_Turret_Encoder = None
        # self.TDCar1LiftLower_Encoder = None
        # self.TDCar2LiftLower_Encoder = None
        # self.DB_Encoder = None
        # self.PR_Encoder = None
        # self.Shear_Angel_Encoder = None
        # self.WSD_Encoder = None
        # self.LevellingRollPos_Encoder = None
        self.setup()






    def setup(self):
        try:
            self.Arm1Lift_Encoder =  Fn_Arm1Lift_Encoder_Encoder(self.filename)
            self.Arm2Lift_Encoder = Fn_Arm2Lift_Encoder_Encoder(self.filename)
            self.BA01_BWL_Turret_Encoder = Fn_BA01_BWL_Turret_Encoder(self.filename)
            self.TDCar1LiftLower_Encoder = Fn_TDCar1LiftLower_Encoder(self.filename)
            self.TDCar2LiftLower_Encoder = Fn_TDCar2LiftLower_Encoder(self.filename)
            self.DB_Encoder = Fn_DB_Encoder_Encoder(self.filename)
            self.PR_Encoder = Fn_PR_Encoder_Encoder(self.filename)
            self.Shear_Angel_Encoder = Fn_Shear_Angel_Encoder(self.filename)
            self.WSD_Encoder = Fn_WSD_Encoder_Encoder(self.filename)
            self.LevellingRollPos_Encoder = Fn_LevellingRollPos_Encoder(self.filename)


        except Exception as e:
            level = logging.ERROR
            messege = 'Event:' + "Cal_AllEncoder" + str(e.args)
            logger.log(level, messege)


    @property
    def arm1Lift_Encoder(self):
        return  self.Arm1Lift_Encoder

    @property
    def arm2Lift_Encoder(self):
        return self.Arm2Lift_Encoder

    @property
    def bA01_BWL_Turret_Encoder(self):
        return self.BA01_BWL_Turret_Encoder

    @property
    def tDCar1LiftLower_Encoder(self):
        return self.TDCar1LiftLower_Encoder

    @property
    def tDCar2LiftLower_Encoder(self):
        return self.TDCar2LiftLower_Encoder

    @property
    def dB_Encoder(self):
        return self.DB_Encoder

    @property
    def pR_Encoder(self):
        return self.PR_Encoder

    @property
    def shear_Angel_Encoder(self):
        return self.Shear_Angel_Encoder

    @property
    def wSD_Encoder(self):
        return self.WSD_Encoder

    @property
    def levellingRollPos_Encoder(self):
        return self.LevellingRollPos_Encoder





