from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import tkinter as tk
from tkinter import *
from time import sleep
from clientcomm_v1 import *
from readgeneral_v2 import *
from  writegeneral_v2 import *






class ControlPanelUi:
    def __init__(self,frame, filename):
        self.frame = frame
        self.client = Communication()
        self.sta_con_plc = self.client.opc_client_connect(filename)
        self.readgeneral = ReadGeneral(self.sta_con_plc)
        self.writegeneral = WriteGeneral(self.sta_con_plc)
        self.setup()


    def setup(self):
        self.startbutton1 = ttk.Button(self.frame, text='Start ID 1', command=self.IDfan1start)
        self.startbutton1.grid(column=0, row=2)

        self.stopbutton1 = ttk.Button(self.frame, text='Stop ID 1', command=self.IDfan1stop)
        self.stopbutton1.grid(column=0, row=3)

        self.resetID1 = ttk.Button(self.frame, text='Reset ID 1', command=self.resetIDfan1)
        self.resetID1.grid(column=0, row=4)

        self.deskon1 = ttk.Button(self.frame, text='Deskon ID 1', command=self.deskon1func)
        self.deskon1.grid(column=0, row=5)

        self.openbutton1 = ttk.Button(self.frame, text='DamperOp ID 1', command=self.IDfan1dampon)
        self.openbutton1.grid(column=0, row=6)

        self.closebutton1 = ttk.Button(self.frame, text='DamperCl ID 1', command=self.IDfan1dampoff)
        self.closebutton1.grid(column=0, row=7)

        self.startbutton2 = ttk.Button(self.frame, text='Start ID 2', command=self.IDfan2start)
        self.startbutton2.grid(column=1, row=2)

        self.stopbutton2 = ttk.Button(self.frame, text='Stop ID 2', command=self.IDfan2stop)
        self.stopbutton2.grid(column=1, row=3)

        self.resetID2 = ttk.Button(self.frame, text='Reset ID 2', command=self.resetIDfan2)
        self.resetID2.grid(column=1, row=4)

        self.deskon2 = ttk.Button(self.frame, text='Deskon ID 2', command=self.deskon2func)
        self.deskon2.grid(column=1, row=5)

        self.openbutton2 = ttk.Button(self.frame, text='DamperOp ID 2', command=self.IDfan2dampon)
        self.openbutton2.grid(column=1, row=6)

        self.closebutton2 = ttk.Button(self.frame, text='DamperCl ID 2', command=self.IDfan2dampoff)
        self.closebutton2.grid(column=1, row=7)

        self.startbutton3 = ttk.Button(self.frame, text='Start ID 3', command=self.IDfan3start)
        self.startbutton3.grid(column=2, row=2)

        self.stopbutton3 = ttk.Button(self.frame, text='Stop ID 3', command=self.IDfan3stop)
        self.stopbutton3.grid(column=2, row=3)

        self.resetID3 = ttk.Button(self.frame, text='Reset ID 3', command=self.resetIDfan3)
        self.resetID3.grid(column=2, row=4)

        self.deskon3 = ttk.Button(self.frame, text='Deskon ID 3', command=self.deskon3func)
        self.deskon3.grid(column=2, row=5)

        self.openbutton3 = ttk.Button(self.frame, text='DamperOp ID 3', command=self.IDfan3dampon)
        self.openbutton3.grid(column=2, row=6)

        self.closebutton3 = ttk.Button(self.frame, text='DamperCl ID 3', command=self.IDfan3dampoff)
        self.closebutton3.grid(column=2, row=7)

        self.deskoff1 = ttk.Button(self.frame, text='Desk off ID 1', command=self.damplocal1)
        self.deskoff1.grid(column=0, row=8)

        self.deskoff2 = ttk.Button(self.frame, text='Desk off ID 2', command=self.damplocal2)
        self.deskoff2.grid(column=1, row=8)

        self.deskoff3 = ttk.Button(self.frame, text='Desk off ID 3', command=self.damplocal3)
        self.deskoff3.grid(column=2, row=8)

    def deskon1func(self):

        self.writegeneral.writesymbolvalue('401.0', 1, 'S7WLBit')

    def deskon2func(self):

        self.writegeneral.writesymbolvalue('401.6', 1, 'S7WLBit')

    def deskon3func(self):

        self.writegeneral.writesymbolvalue('402.4', 1, 'S7WLBit')

    def damplocal1(self):

        self.writegeneral.writesymbolvalue('401.0', 0, 'S7WLBit')

    def damplocal2(self):

        self.writegeneral.writesymbolvalue('401.6', 0, 'S7WLBit')

    def damplocal3(self):

        self.writegeneral.writesymbolvalue('402.4', 0, 'S7WLBit')

    def IDfan1start(self):

        self.writegeneral.writesymbolvalue('401.1', 1,'S7WLBit')
        self.writegeneral.writesymbolvalue('401.2', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('401.1', 0, 'S7WLBit')

    def IDfan1stop(self):

        self.writegeneral.writesymbolvalue('401.2', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.1', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('401.2', 0, 'S7WLBit')

    def IDfan1dampon(self):

        self.writegeneral.writesymbolvalue('401.3', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.4', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('401.3', 0, 'S7WLBit')

    def IDfan1dampoff(self):

        self.writegeneral.writesymbolvalue('401.4', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.3', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('401.4', 0, 'S7WLBit')

    def IDfan2start(self):

        self.writegeneral.writesymbolvalue('401.7', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.0', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('401.7', 0, 'S7WLBit')

    def IDfan2stop(self):

        self.writegeneral.writesymbolvalue('402.0', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.7', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('402.0', 0, 'S7WLBit')


    def IDfan2dampon(self):

        self.writegeneral.writesymbolvalue('402.1', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.2', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('402.1', 0, 'S7WLBit')

    def IDfan2dampoff(self):

        self.writegeneral.writesymbolvalue('402.2', 1,'S7WLBit')
        self.writegeneral.writesymbolvalue('402.1', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('402.2', 0, 'S7WLBit')

    def IDfan3start(self):

        self.writegeneral.writesymbolvalue('402.5', 1,'S7WLBit')
        self.writegeneral.writesymbolvalue('402.6', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('402.5', 0, 'S7WLBit')

    def IDfan3stop(self):

        self.writegeneral.writesymbolvalue('402.6', 1, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.5', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('402.6', 0, 'S7WLBit')

    def IDfan3dampon(self):

        self.writegeneral.writesymbolvalue('402.7', 1,'S7WLBit')
        self.writegeneral.writesymbolvalue('403.0', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('402.7', 0, 'S7WLBit')

    def IDfan3dampoff(self):

        self.writegeneral.writesymbolvalue('403.0', 1,'S7WLBit')
        self.writegeneral.writesymbolvalue('402.7', 0, 'S7WLBit')
        sleep(.5)
        self.writegeneral.writesymbolvalue('403.0', 0, 'S7WLBit')


    def resetIDfan1(self):

        self.writegeneral.writesymbolvalue('401.1', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.2', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.3', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.4', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.0', 0, 'S7WLBit')
        # self.gen.writegeneral.writesymbolvalue('25.2', 1, 'S7WLBit')

    def resetIDfan2(self):

        self.writegeneral.writesymbolvalue('401.7', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.0', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.1', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.2', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('401.6', 0, 'S7WLBit')
        # self.gen.writegeneral.writesymbolvalue('26.3', 1, 'S7WLBit')

    def resetIDfan3(self):

        self.writegeneral.writesymbolvalue('402.5', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.6', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.7', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('403.0', 0, 'S7WLBit')
        self.writegeneral.writesymbolvalue('402.4', 0, 'S7WLBit')
        # self.gen.writegeneral.writesymbolvalue('27.4', 1, 'S7WLBit')





class Fn_ControlPanel:
    def __init__(self,frame,filename):
        self.filename = filename
        self.frame = frame
        self.win = tk.Toplevel(self.frame)
        self.win.geometry('500x250')
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)
        vertical_pane = ttk.PanedWindow(self.win, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)

        controlpanel_frame = ttk.Labelframe(horizontal_pane, text="Control Panel")
        controlpanel_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(controlpanel_frame, weight=1)


        # Initialize all frames
        self.controlpanelui = ControlPanelUi(controlpanel_frame,self.filename)







