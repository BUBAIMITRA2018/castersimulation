import tkinter as tk
import tkinter.ttk as ttk
import AutocompleteCombox
import pandas as pd

df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='Encoder')
root = tk.Tk()
win = tk.Toplevel(root)
win.geometry("250x200")

def collectwritetaglist():
    listofdevice = []
    listofencoderoutputtags = []
    n = 0
    while n < len(df.index):
        listofdevice.append(df.iloc[n, 0])
        listofencoderoutputtags.append(df.iloc[n,7])
        n = n + 1
    return listofdevice,listofencoderoutputtags

def update():
    for i in range(0, len(df.index)):
        print("tagname is :", tagname_entered.get())
        if tagname_entered.get() == df.iloc[i, 0]:
            df.iloc[i,6] = fastcount.get()

def insert_data():
    for i in range(0,len(df.index)):
        print("tagname is :",tagname_entered.get())
        if tagname_entered.get() == df.iloc[i,0]:
            text_box.insert("end-1c", str(df.iloc[i,7]))

listofencoderdevices,listofencoderoutputtags = collectwritetaglist()
ttk.Label(win, text='Choose Encoder').grid(column=0, row=1)
tagname_entered = AutocompleteCombox.AutocompleteCombobox(win, width=18)
tagname_entered.grid(column=2, row=1)
tagname_entered.set_completion_list(listofencoderdevices)
tagname_entered.focus_set()
ttk.Label(win, text='EncoderTag').grid(column=0, row=5)
ttk.Button(win,text = "Submit",command = insert_data).grid(column=0,row =6)
text_box = tk.Text(win, width = 17, height = 1)
text_box.grid(row = 5, column = 2, columnspan = 2)
ttk.Label(win, text='Calibrated Value').grid(column=0, row=7)
calibration_value = tk.IntVar()
tagvalue = ttk.Entry(win, width=22, textvariable=calibration_value)
tagvalue.grid(column=2, row=7)
ttk.Label(win, text='FastCount').grid(column=0, row=8)
fastcountvalue = tk.IntVar()
fastcount = ttk.Entry(win, width=22, textvariable=fastcountvalue)
fastcount.grid(column=2, row=8)
ttk.Button(win,text = "update",command = insert_data).grid(column=0,row =9)
root.mainloop()
