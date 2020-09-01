import threading
import callalloutsignals_V3
import callallvibrofeeder_V3
import callallmotor2D_V3
import callallramp_V3
import callallsov1S_V3
import pandas as pd

import tkinter as tk
from tkinter import filedialog
class AllDevices:

    def __init__(self,comobject,import_file_path):

        self.comobject = comobject


        self.dfVF  = pd.read_excel(import_file_path, sheet_name='VibroFeeder')
        self.dfM2D = pd.read_excel(import_file_path, sheet_name='Motor2D')
        self.dframpsignal = pd.read_excel(import_file_path, sheet_name='Ramp')
        self.dfoutsignal = pd.read_excel(import_file_path, sheet_name='OutputTx')
        self.dfS1S = pd.read_excel(import_file_path, sheet_name='Valve1S')


        #

        self.allvfobjects =   callallvibrofeeder_V3.Cal_AllVibroFeeder(self.dfVF,comobject,import_file_path)
        self.rampobjects  = callallramp_V3.Cal_AllRampInputs(self.dframpsignal,comobject,import_file_path)
        self.allmotor2dobjects = callallmotor2D_V3.Cal_AllMotor2D(self.dfM2D, comobject, import_file_path)
        self.alloutsignalobjects = callalloutsignals_V3.Cal_AllOutsingnal(self.dfoutsignal, comobject, import_file_path)
        self.allsov1sobjects = callallsov1S_V3.Cal_AllSov1S(self.dfS1S, comobject, import_file_path)






    #
    #
    @property
    def allsov1s(self):
        return self.allsov1sobjects


    #
    @property
    def allvibrofeeders(self):
        return self.allvfobjects



    @property
    def allrampobjects(self):
        return self.rampobjects

    @property
    def allmotor2d(self):
        return self.allmotor2dobjects



