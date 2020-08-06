import tkinter as tk
import tkinter.ttk as ttk
import AutocompleteCombox
import openpyxl


class Encoder_Operation:
    def __init__(self,root,gen,alldevices):
        self.root = root
        self.gen = gen
        self.alldevices = alldevices

        self.setup()

    def update(self):

        for i in range(0, len(self.alldevices.allsiemensdrives.listofdrive1Dir)):
                print("Hi i am here ")
                if self.tagname_entered.get() == self.alldevices.allsiemensdrives.listofdrive1Dir[i].devicename:
                    value = int(self.tagvalue.get())
                    self.gen.writegeneral.writesymbolvalue(self.alldevices.allsiemensdrives.listofdrive1Dir[i].encoderoutputtag, value, 'S7WLWord')
                    self.alldevices.allsiemensdrives.listofdrive1Dir[i].fastcount = int(self.fastcount.get())

        print("fasttag value is :",self.alldevices.allsiemensdrives.listofdrive1Dir[0].fastcount )


    def insert_data(self):
        for i in range(0, len(self.alldevices.allsiemensdrives.listofdrive1Dir)):
            if self.tagname_entered.get() == self.alldevices.allsiemensdrives.listofdrive1Dir[i].devicename:
                print(self.alldevices.allsiemensdrives.listofdrive1Dir[i].encoderoutputtag)
                self.text_box.insert("end-1c", str(self.alldevices.allsiemensdrives.listofdrive1Dir[i].encoderoutputtag))



    def setup(self):
        self.win = tk.Toplevel(self.root)
        self.win.geometry("250x200")
        print("number of devices :",self.alldevices.allsiemensdrives)
        listofencoderdevices, listofencoderoutputtags = self.collectwritetaglist()
        ttk.Label(self.win, text='Choose Encoder').grid(column=0, row=1)
        self.tagname_entered = AutocompleteCombox.AutocompleteCombobox(self.win, width=18)
        self.tagname_entered.grid(column=2, row=1)
        self.tagname_entered.set_completion_list(listofencoderdevices)
        self.tagname_entered.focus_set()
        ttk.Label(self.win, text='EncoderTag').grid(column=0, row=5)
        ttk.Button(self.win, text="Submit", command=self.insert_data).grid(column=0, row=6)
        self.text_box = tk.Text(self.win, width=17, height=1)
        self.text_box.grid(row=5, column=2, columnspan=2)
        ttk.Label(self.win, text='Calibrated Value').grid(column=0, row=7)
        calibration_value = tk.IntVar()
        self.tagvalue = ttk.Entry(self.win, width=22, textvariable=calibration_value)
        self.tagvalue.grid(column=2, row=7)
        ttk.Label(self.win, text='FastCount').grid(column=0, row=8)
        fastcountvalue = tk.IntVar()
        ttk.Button(self.win, text="update", command=self.update).grid(column=0, row=10)
        self.root.mainloop()

    def collectwritetaglist(self):
        self.listofdevice = []
        self.listofencoderoutputtags = []
        n = 0
        self.fastcount = ttk.Entry(self.win, width=22, textvariable='fastcountvalue')
        self.fastcount.grid(column=2, row=8)
        while n < len( self.alldevices.allsiemensdrives.listofdrive1Dir):
            self.listofdevice.append(self.alldevices.allsiemensdrives.listofsiemensdrive1D[n].devicename)
            print("siemens drives " ,self.alldevices.allsiemensdrives.listofsiemensdrive1D[n].devicename)
            self.listofencoderoutputtags.append(self.alldevices.allsiemensdrives.listofsiemensdrive1D[n].encoderoutputtag)
            n = n + 1
        return self.listofdevice, self.listofencoderoutputtags













