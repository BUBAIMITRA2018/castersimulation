import threading
import calalldummybar_V3
import pandas as pd
import tkinter as tk
from tkinter import filedialog
class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject


        self.dfdummybar = pd.read_excel(import_file_path, sheet_name='DummyBar')


        self.alldummybarobjects = calalldummybar_V3.Cal_AllDummyBar(self.dfdummybar, comobject,import_file_path)





    #
    #
    # def __deepcopy__(self, memo):
    #     newself = self.__class__.__new__(self.__class__)
    #     for name, value in vars(self).items():
    #         if name != 'mylock':
    #             value = copy.deepcopy(value)
    #         setattr(newself, name, value)
    #     return newself



    @property
    def alldummybar(self):
        return self.alldummybarobjects
