import threading
import callallmotor1D_V3
import callallmotor2D_V3
import callallsov1S_V3
import callallsov2S_V3
import callallvibrofeeder_V3
import callallconveyor_V3
import  calallABPdrives_V3
import  callallEncoder_V3
import callalloutsignals_V3
import  callallsiemensdrive1D_V3
import  callalldigital_V3
import calallcontrolvalves_V3
import calalldummybar_V3
import pandas as pd

import calallanalog_V3
import tkinter as tk
from tkinter import filedialog
class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject

        self.dfM1D = pd.read_excel( import_file_path, sheet_name='Motor1D')
        self.dfM2D = pd.read_excel(import_file_path, sheet_name='Motor2D')
        self.dfS1S = pd.read_excel(import_file_path, sheet_name='Valve1S')
        self.dfS2S =  pd.read_excel(import_file_path, sheet_name='Valve2S')
        self.dfVF  = pd.read_excel(import_file_path, sheet_name='VibroFeeder')
        self.dfCONV = pd.read_excel(import_file_path, sheet_name='Conveyor')
        self.dfdrive = pd.read_excel(import_file_path, sheet_name='Drive')
        # self.dfencoder = pd.read_excel(import_file_path, sheet_name='Encoder')
        self.dfoutsignal = pd.read_excel(import_file_path, sheet_name='OutputTx')
        self.dfanalog = pd.read_excel(import_file_path, sheet_name='AnalogTx')
        self.dfsiemensdrive = pd.read_excel(import_file_path, sheet_name='SiemensDrive')
        self.dfdigitalsignal = pd.read_excel(import_file_path, sheet_name='DigitalTx')
        self.dfcontrolvalve = pd.read_excel(import_file_path, sheet_name='ControlValves')
        self.dfdummybar = pd.read_excel(import_file_path, sheet_name='DummyBar')

        self.allmotor1dobjects = callallmotor1D_V3.Cal_AllMotor1D(self.dfM1D, comobject,import_file_path)
        self.allmotor2dobjects = callallmotor2D_V3.Cal_AllMotor2D(self.dfM2D, comobject,import_file_path)
        self.allsov1sobjects = callallsov1S_V3.Cal_AllSov1S(self.dfS1S,comobject,import_file_path)
        # self.allsov2sobjects =  callallsov2S_V3.Cal_AllSov2S(self.dfS2S,comobject)
        # self.allvfobjects =   callallvibrofeeder_V3.Cal_AllVibroFeeder(self.dfVF,comobject)
        # self.allconveyorobjects = callallconveyor_V3.Cal_AllConveyor1D(self.dfCONV,comobject)
        # self.alldriveobjects = calallABPdrives_V3.Cal_ABBDrives(self.dfdrive,comobject)
        # # self.allencoderobjects = callallEncoder_V3.Cal_AllEncoder(self.dfencoder,comobject)
        self.alloutsignalobjects = callalloutsignals_V3. Cal_AllOutsingnal(self.dfoutsignal, comobject,import_file_path)
        # self.allanalogsignalobjects = calallanalog_V3.Cal_AllAnalogInputs(self.dfanalog,comobject,import_file_path)
        self.allsiemensdrivesobjects = callallsiemensdrive1D_V3.Cal_AllSiemensDrive1D(self.dfsiemensdrive,comobject,import_file_path)
        # self.alldigitalsignalobjects = callalldigital_V3.Cal_AllDigital(self.dfdigitalsignal,comobject)
        self.allcontrolvalveobjects = calallcontrolvalves_V3.Cal_AllControlValves(self.dfcontrolvalve,comobject,import_file_path)
        self.alldummybarobjects = calalldummybar_V3.Cal_AllDummyBar(self.dfdummybar, comobject,import_file_path)    #
    #
    # def __deepcopy__(self, memo):
    #     newself = self.__class__.__new__(self.__class__)
    #     for name, value in vars(self).items():
    #         if name != 'mylock':
    #             value = copy.deepcopy(value)
    #         setattr(newself, name, value)
    #     return newself

    @property
    def allmotor1d(self):
        return self.allmotor1dobjects

    @property
    def allmotor2d(self):
        return self.allmotor2dobjects
    #
    @property
    def allsov1s(self):
        return self.allsov1sobjects

    @property
    def alldummybar(self):
        return self.alldummybarobjects

    # @property
    # def allsov2s(self):
    #     return self.allsov2sobjects
    #
    # @property
    # def allvibrofeeders(self):
    #     return self.allvfobjects
    #
    # @property
    # def allconveyors(self):
    #     return self.allconveyorobjects
    #
    # @property
    # def alldrives(self):
    #     return self.alldriveobjects
    # @property
    # def allanalogs(self):
    #     return self.allanalogsignalobjects

    # # @property
    # # def allencoders(self):
    # #     return self.allencoderobjects
    #
    @property
    def allsiemensdrives(self):
        return self.allsiemensdrivesobjects

    # @property
    # def alldigitalsignals(self):
    #     return self.alldigitalsignalobjects

    @property
    def allcontrolvalves(self):
        return self.allcontrolvalveobjects



