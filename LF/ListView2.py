from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk




class MultiColumnListbox():
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self,root,elementheader):
        self.tree = ''
        self._root = root
        self._detached = set()
        self.element_header= elementheader
        self._setup_widgets()




    def _setup_widgets(self):
        win2 = Toplevel(self._root)
        win2.geometry('650x250')

        win2.resizable(width=0, height=0)
        message = "Read General"
        Label(win2, text=message).pack()
        new_element_header = [self.element_header[0], self.element_header[1]]

        self.tree = ttk.Treeview(win2, columns=new_element_header, show="headings", selectmode='browse')
        self.tree.pack(side='left',pady=2)

        r = Label(win2, text="Search", fg="red")
        r.pack()


        self.tree.heading(self.element_header[0], text=self.element_header[0])
        self.tree.heading(self.element_header[1], text=self.element_header[1])

        vsb = ttk.Scrollbar(win2,orient="vertical",
                            command=self.tree.yview)
        vsb.pack(side='left', fill='y')

        hsb = ttk.Scrollbar(win2,orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                       xscrollcommand=hsb.set)

        vcmd = (win2.register(self._columns_searcher), '%P')
        self.entry = tk.Entry(win2, bd=10, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=2)



    def search(self,item = ''):
        print("hihihi")

        children = self.tree.get_children(item)
        for child in children:
            text = self.tree.item(child,'text')
            if text.startswith(self.entry.get()):
                self.tree.selection_set(child)
                print("Hi1")
                return True
            else:
                res = self.search(child)
                print("child:",child)
                print("child:", res)

                print("Hi2")
                if res:
                    return True



    def _build_tree(self,element_list):
        print("I am here")
        self.tree.delete(*self.tree.get_children())
        for col in self.element_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: treeview_sort_column(self.tree,c,False))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in element_list:

            # children = self.tree.get_children(item)
            # print(children)
            self.tree.insert('', 'end', values=item)
            # for child in children:
            #     if child == item :
            #         exit()
            #     else:
            #         self.tree.insert('', 'end', values=item)

            # adjust column's width if necessary to fit each value

            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.element_header[ix],width=None)<col_w:
                    self.tree.column(self.element_header[ix], width=col_w)

    def _columns_searcher(self, P):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        self._brut_searcher(children, P)
        return True

    def _brut_searcher(self, children, query):
        i_r = -1
        try:
            for item_id in children:
                text = self.tree.item(item_id)["values"][0]
                if query.upper() in str(text).upper():
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)
        except:
            pass


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))





def sortby(tree, col, descending):

    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

# the test data ...




if __name__ == '__main__':
    element_header= ['car', 'repair']
    element_list = [
        ('Hyundai', 'brakes'),
        ('Honda', 'light'),
        ('Lexus', 'battery'),
        ('Benz', 'wiper'),
        ('Ford', 'tire'),
        ('Chevy', 'air'),
        ('Chrysler', 'piston'),
        ('Toyota', 'brake pedal'),
        ('BMW', 'seat')
    ]

    root = Tk()
    listbox = MultiColumnListbox(root,element_header)
    listbox._build_tree(element_list)
    root.mainloop()
