# import tkinter as tk
# import tkinter.ttk as ttk
# import AutocompleteCombox
# from pandas import ExcelWriter
# from pandas import ExcelFile
# import openpyxl
# import numpy as np
# import pandas as pd
#
# class Analog_Operation:
#     def __init__(self,root,gen,alldevice):
#         self.root = root
#         self.gen = gen
#         self.alldevice = alldevice
#         # self.writer = ExcelWriter('Working_VF1_5.xls', engine='xlsxwriter')
#         # print(self.writer)
#         self.setup()
#
#     def update(self):
#             for i in range(0, len(self.df.index)):
#                 print("tagname is :", self.tagname_entered.get())
#                 if self.tagname_entered.get() == self.df.iloc[i, 0]:
#                     # Open existing excel file
#                     self.df.iloc[i, 3] = self.fastcount.get()
#                     print("fastcount is :",self.fastcount.get())
#                     self.df.to_excel(self.writer,sheet_name="Encoder")
#                     self.writer.save()
#
#     def insert_data(self):
#         for i in range(0, len(self.  self.outputtag )):
#             print("tagname is :", self.tagname_entered.get())
#             if self.tagname_entered.get() == self.df.iloc[i, 0]:
#                 self.text_box.insert("end-1c", str(self.df.iloc[i, 7]))
#
#     def setup(self):
#         self.win = tk.Toplevel(self.root)
#         self.win.geometry("250x200")
#         listofanalogdevices, listofanalogoutputtags = self.collectwritetaglist()
#         ttk.Label(self.win, text='Choose Encoder').grid(column=0, row=1)
#         self.tagname_entered = AutocompleteCombox.AutocompleteCombobox(self.win, width=18)
#         self.tagname_entered.grid(column=2, row=1)
#         self.tagname_entered.set_completion_list(listofanalogdevices)
#         self.tagname_entered.focus_set()
#         ttk.Label(self.win, text='Analog Tag').grid(column=0, row=5)
#         ttk.Button(self.win, text="Submit", command=self.insert_data).grid(column=0, row=6)
#         self.text_box = tk.Text(self.win, width=17, height=1)
#         self.text_box.grid(row=5, column=2, columnspan=2)
#         ttk.Label(self.win, text='Calibrated Value').grid(column=0, row=7)
#         calibration_value = tk.IntVar()
#         tagvalue = ttk.Entry(self.win, width=22, textvariable=calibration_value)
#         tagvalue.grid(column=2, row=7)
#         ttk.Label(self.win, text='FastCount').grid(column=0, row=8)
#         fastcountvalue = tk.IntVar()
#         self.fastcount = ttk.Entry(self.win, width=22, textvariable=fastcountvalue)
#         self.fastcount.grid(column=2, row=8)
#         ttk.Button(self.win, text="update", command=self.update).grid(column=0, row=9)
#         self.root.mainloop()
#
#     def collectwritetaglist(self):
#         self.listofdevice = []
#         self.listofencoderoutputtags = []
#         n = 0
#         while n < len(self.alldevice.allanalogsignalobjects):
#             self.listofdevice.append(self.alldevice.allanalogsignalobjects[n])
#             self.listofencoderoutputtags.append(self.alldevice.allanalogsignalobjects[n]. self.outputtag )
#             n = n + 1
#         return self.listofdevice, self.listofencoderoutputtags
#
#
# if __name__ == '__main__':
#      # root = tk.Tk()
#      # gen = int(1)
#      # encoderoperation = Encoder_Operation(root,gen)
#      import openpyxl
#      myworkbook = openpyxl.load_workbook('C:/OPCUA/Working_VF1_5.xls')
#      worksheet = myworkbook.get_sheet_by_name('Encoder')
#      worksheet['B4'] = 'We are writing to B4'
#      mycell = worksheet['B4']
#      mycell.value = 'Writing with reference to cell'
#
#
#
#
#
#
#
#
#
#
#
