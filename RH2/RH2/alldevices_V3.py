import threading
import callallsov1S_V3
import callallmotor1D_V3
import  callallmotor2D_V3
import callallsov2S_V3
import calallanalog_V3
import pandas as pd
import calallcontrolvalves_V3
import callalloutsignals_V3
import callallvibrofeeder_V3
import callallsiemensdrive1D_V3
import callalldigital_V3



class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject
        self.dfS1S = pd.read_excel(import_file_path, sheet_name='Valve1S')
        self.dfS2S = pd.read_excel(import_file_path, sheet_name='Valve2S')
        self.dfM1D = pd.read_excel(import_file_path, sheet_name='Motor1D')
        self.dfM2D = pd.read_excel(import_file_path, sheet_name='Motor2D')
        self.dfANA = pd.read_excel(import_file_path, sheet_name='AnalogTx')
        self.dfCON = pd.read_excel(import_file_path,sheet_name='ControlValves')
        self.dfoutsignal = pd.read_excel(import_file_path,sheet_name='OutputTx')
        self.dfvibrofeeder = pd.read_excel(import_file_path,sheet_name='VibroFeeder')
        self.dfsiemensdrive = pd.read_excel(import_file_path, sheet_name='SiemensDrive')
        self.dfdigitalsignal = pd.read_excel(import_file_path, sheet_name='DigitalTx')


        self.allsov1sobjects = callallsov1S_V3.Cal_AllSov1S(self.dfS1S,comobject,import_file_path)
        self.allmtor1dobjects = callallmotor1D_V3.Cal_AllMotor1D(self.dfM1D, comobject,import_file_path)
        self.allsov2sobjects =  callallsov2S_V3.Cal_AllSov2S(self.dfS2S,comobject,import_file_path)
        self.allmotor2dobjects = callallmotor2D_V3.Cal_AllMotor2D(self.dfM2D, comobject, import_file_path)
        self.allanalogobjects = calallanalog_V3.Cal_AllAnalogInputs(self.dfANA,comobject,import_file_path)
        self.allcontrolvalveobjects =  calallcontrolvalves_V3.Cal_AllControlValves(self.dfCON,comobject,import_file_path)
        self.alloutsignalobjects =  callalloutsignals_V3.Cal_AllOutsingnal(self.dfoutsignal,comobject,import_file_path)
        # self.allvibrofeederobjects = callallvibrofeeder_V3.Cal_AllVibroFeeder(self.dfvibrofeeder,comobject,import_file_path)
        self.allsiemensdrivesobjects = callallsiemensdrive1D_V3.Cal_AllSiemensDrive1D(self.dfsiemensdrive,comobject,import_file_path)
        self.alldigitalsignalobjects = callalldigital_V3.Cal_AllDigital(self.dfdigitalsignal, comobject, import_file_path)





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

    @property
    def allanalogsignalobjects(self):
        return self.allanalogobjects

    @property
    def allcontrolvalves(self):
        return self.allcontrolvalveobjects

    @property
    def allvibrofeeder(self):
        return self.allvibrofeederobjects

    @property
    def alldigitalsignals(self):
        return self.alldigitalsignalobjects

    @property
    def allsiemensdrives(self):
        return self.allsiemensdrivesobjects

    @property
    def allrampobjects(self):
        return self.allrampsignalobjects










