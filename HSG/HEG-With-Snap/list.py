import tkinter as tk
import tkinter.ttk
import pandas as pd

def collectwritetaglist():
    list1 = []
    df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='WriteGeneral')
    n = 0
    while n < len(df.index):
        list1.append(df.iloc[n, 0])
        n = n + 1
    return list1

def select():
    curItems = tree.selection()
    lb = tk.Label(root,text = "\n".join([str(tree.item(i)['values']) for i in curItems])).pack()

    # lb = tk.Label(root,text = "\n".join([str(tree.item(i)['values']) for i in curItems])).pack())
    print(curItems)
    # lb = tk.Label(root, text="\n".join([str(tree.item(i)['values']) for i in curItems])).pack())
    # lb.pack()

# "\n".join([str(tree.item(i)['values']) for i in curItems])).pack()
root = tk.Tk()
tree = tkinter.ttk.Treeview(root, height=4)
listofwritetag = collectwritetaglist()

tree['show'] = 'headings'
tree['columns'] = ('Tag Name', 'Value')
tree.heading("#1", text='Tag Name', anchor='w')
tree.column("#1", stretch="no")
tree.heading("#2", text='Value', anchor='w')
tree.column("#2", stretch="no")
tree.pack()

n = 0
while n < len(listofwritetag):
    tree.insert("", n, values=[listofwritetag[n], 1 ])
    n = n + 1

tree.bind("<Double-1>", lambda e: select())
root.mainloop()