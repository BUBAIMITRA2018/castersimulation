
from callallencoder import *


logger = logging.getLogger("main.log")



class Allencoderprocess:
    def __init__(self,filename):
        self.filename = filename
        self.allencoder = Cal_AllEncoder(self.filename)

    def arm1Lift_Encoder_process(self):
        self.allencoder.arm1Lift_Encoder.encoderprocess()

    def arm2Lift_Encoder_process(self):
        self.allencoder.arm2Lift_Encoder.encoderprocess()

    def bA01_BWL_Turret_Encoder(self):
        self.allencoder.bA01_BWL_Turret_Encoder.encoderprocess()

    def dB_Encoder(self):
        self.allencoder.dB_Encoder.encoderprocess()

    def pR_Encoder(self):
        self.allencoder.pR_Encoder.encoderprocess()

    def shear_Angel_Encoder(self):
        self.allencoder.shear_Angel_Encoder.encoderprocess()

    def wSD_Encoder(self):
        self.allencoder.wSD_Encoder.encoderprocess()

    def lvellingRollPos_Encoder(self):
        self.allencoder.levellingRollPos_Encoder.encoderprocess()

    def tDCar1LiftLower_Encoder(self):
        self.allencoder.tDCar1LiftLower_Encoder.encoderprocess()

    def tDCar2LiftLower_Encoder(self):
        self.allencoder.tDCar2LiftLower_Encoder.encoderprocess()





















