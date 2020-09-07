import threading
import pandas as pd
import callallramp_V3


class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.comobject = comobject
        self.dframpsignal  = pd.read_excel(import_file_path, sheet_name = 'Ramp')
        self.allrampsignalobjects = callallramp_V3.Cal_AllRampInputs(self.dframpsignal, comobject,import_file_path)


    @property
    def allrampobjects(self):
        return self.allrampsignalobjects










