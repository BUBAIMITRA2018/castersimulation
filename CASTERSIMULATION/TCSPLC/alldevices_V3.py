import threading
import callallcylinder_V3
import callallmotor1D_V3
import callallmotor2D_V3
import callallsov1S_V3
import callallsov2S_V3
import callalloutsignals_V3
import  callalldigital_V3
import calallcontrolvalves_V3


import pandas as pd
class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject

        self.dfcyl = pd.read_excel(import_file_path, sheet_name='Cylinder')
        self.dfM1D = pd.read_excel(import_file_path, sheet_name='Motor1D')
        self.dfM2D = pd.read_excel(import_file_path, sheet_name='Motor2D')
        self.dfS1S = pd.read_excel(import_file_path, sheet_name='Valve1S')
        self.dfS2S = pd.read_excel(import_file_path, sheet_name='Valve2S')
        self.dfoutsignal = pd.read_excel(import_file_path, sheet_name='OutputTx')
        self.dfanalog = pd.read_excel(import_file_path, sheet_name='AnalogTx')
        self.dfdigitalsignal = pd.read_excel(import_file_path, sheet_name='DigitalTx')
        self.dfcontrolvalve = pd.read_excel(import_file_path, sheet_name='ControlValves')


        # self.allmotor1dobjects = callallmotor1D_V3.Cal_AllMotor1D(self.dfM1D, comobject,import_file_path)
        # self.allmotor2dobjects = callallmotor2D_V3.Cal_AllMotor2D(self.dfM2D, comobject,import_file_path)
        # self.allsov1sobjects = callallsov1S_V3.Cal_AllSov1S(self.dfS1S, comobject, import_file_path)
        # self.allsov2sobjects = callallsov2S_V3.Cal_AllSov2S(self.dfS2S, comobject, import_file_path)
        self.alloutsignalobjects = callalloutsignals_V3. Cal_AllOutsingnal(self.dfoutsignal, comobject,import_file_path)
        # self.allanalogsignalobjects = calallanalog_V3.Cal_AllAnalogInputs(self.dfanalog, comobject, import_file_path)
        self.alldigitalsignalobjects = callalldigital_V3.Cal_AllDigital(self.dfdigitalsignal,comobject,import_file_path)
        self.allcontrolvalveobjects = calallcontrolvalves_V3.Cal_AllControlValves(self.dfcontrolvalve, comobject,import_file_path)
        self.allcylindersobjects = callallcylinder_V3.Cal_AllCylinder(self.dfcyl, comobject, import_file_path)






    # @property
    # def allsov1s(self):
    #     return self.allsov1sobjects

    @property
    def allcylinder(self):
        return self.allcylindersobjects
    #
    # @property
    # def allmotor1d(self):
    #     return self.allmotor1dobjects
    #
    # @property
    # def allmotor2d(self):
    #     return self.allmotor2dobjects
    #
    # #
    # @property
    # def allsov1s(self):
    #     return self.allsov1sobjects
    #
    # @property
    # def allsov2s(self):
    #     return self.allsov2sobjects
    #
    #
    # @property
    # def allanalogs(self):
    #     return self.allanalogsignalobjects

    #
    @property
    def alldigitalsignals(self):
        return self.alldigitalsignalobjects

    @property
    def allcontrolvalves(self):
        return self.allcontrolvalveobjects





