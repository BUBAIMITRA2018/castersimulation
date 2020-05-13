import threading
import callallsov1S_V3
import callallmotor1D_V3
import  callallmotor2D_V3
import callallsov2S_V3
import pandas as pd


class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject
        self.dfS1S = pd.read_excel(import_file_path, sheet_name='Valve1S')
        self.dfS2S = pd.read_excel(import_file_path, sheet_name='Valve2S')
        self.dfM1D = pd.read_excel(import_file_path, sheet_name='Motor1D')
        self.dfM2D = pd.read_excel(import_file_path, sheet_name='Motor2D')

        self.allsov1sobjects = callallsov1S_V3.Cal_AllSov1S(self.dfS1S,comobject,import_file_path)
        self.allmtor1dobjects = callallmotor1D_V3.Cal_AllMotor1D(self.dfM1D, comobject,import_file_path)
        self.allsov2sobjects =  callallsov2S_V3.Cal_AllSov2S(self.dfS2S,comobject,import_file_path)
        self.allmotor2dobjects = callallmotor2D_V3.Cal_AllMotor2D(self.dfM2D, comobject, import_file_path)



    @property
    def allsov1s(self):
        return self.allsov1sobjects

    @property
    def allmotor1d(self):
        return self.allmtor1dobjects

    @property
    def allsov2s(self):
        return self.allsov2sobjects

    @property
    def allmotor2d(self):
        return self.allmotor2dobjects

