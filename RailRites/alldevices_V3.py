import threading

import callallmotor2D_V3
import callalloutsignals_V3

import calallSchneiderdrives_V3

import pandas as pd

import calallanalog_V3
import tkinter as tk
from tkinter import filedialog
class AllDevices:

    def __init__(self,comobject,import_file_path):
        self.mylock = threading.Lock()
        self.comobject = comobject


        self.dfM2D = pd.read_excel(import_file_path, sheet_name='Motor2D')

        self.dfoutsignal = pd.read_excel(import_file_path, sheet_name='OutputTx')

        self.dfscheider = pd.read_excel(import_file_path,sheet_name="SchneiderDrive")



        self.allmotor2dobjects = callallmotor2D_V3.Cal_AllMotor2D(self.dfM2D, comobject,import_file_path)

        self.alloutsignalobjects = callalloutsignals_V3. Cal_AllOutsingnal(self.dfoutsignal, comobject,import_file_path)

        self.allscheiderobjects = calallSchneiderdrives_V3.Cal_SchneiderDrives(self.dfscheider,comobject,import_file_path)




    @property
    def allmotor2d(self):
        return self.allmotor2dobjects

    @property
    def allschneiders(self):
        return self.allscheiderobjects



