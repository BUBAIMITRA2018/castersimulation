import tkinter as tk
import pandas as pd
import general
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W, DISABLED, NORMAL


class EncoderCalibration:
    def __init__(self,root,df,idx_no,col_no,gen):
        self.root = root
        self.df = df
        self.idx_no = idx_no
        self.col_no = col_no
        self.gen = gen
        self.setup()


    def setup(self):
        self.title = str(self.df.iloc[self.idx_no,0])
        win = tk.Toplevel(self.root)
        win.geometry("200x50")
        win.title(self.title)
        # create the listbox (note that size is in characters)
        listbox1 = tk.Listbox(win, width=50, height=6)
        listbox1.grid(row=0, column=0)

        # create a vertical scrollbar to the right of the listbox
        yscroll = tk.Scrollbar(command=listbox1.yview, orient=tk.VERTICAL)
        yscroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        listbox1.configure(yscrollcommand=yscroll.set)

        # use Label widget to make heading
        label1 = tk.Label(listbox1, width=12, text="Calibration Value", bg='white')
        label1.grid(row=1, column=0)

        # use entry widget to display/edit selection
        value = tk.IntVar()
        self.enter1 = tk.Entry(listbox1, width=15, textvariable=value, bg='white')
        self.enter1.grid(row=1, column=1)

        button1 = tk.Button(listbox1, text='Calibration ', command=self.calibration)
        button1.grid(row=2, column=0, sticky=tk.W)


    def calibration(self):
        tagname = self.df.iloc[self.idx_no, self.col_no]
        self.gen.writegeneral.writenodevalue(tagname, self.enter1)





if __name__ == "__main__":
    root = tk.Tk()
    df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='Encoder')
    gen = int(1)
    n = 0
    while n < len(df.index):
        print(len(df.index))
        df.iloc[n, 0] = EncoderCalibration(root,df,n,4,gen)
        n = n + 1
    root.mainloop()

