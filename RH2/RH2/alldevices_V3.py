import threading
import callallsov1S_V3
import pandas as pd


class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject
        self.dfS1S = pd.read_excel(import_file_path, sheet_name='Valve1S')
        self.allsov1sobjects = callallsov1S_V3.Cal_AllSov1S(self.dfS1S,comobject,import_file_path)



    @property
    def allsov1s(self):
        return self.allsov1sobjects



