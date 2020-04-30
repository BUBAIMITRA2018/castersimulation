# Import
import tkinter as Tkinter
import tkinter.ttk as ttk

# Class
class App:

    # Init
    def __init__(self):
        self.options = ["All", "Odd", "Even"] # Combobox elements
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # Treeview elements

        self.last_filter_mode = "" # Combobox change detector

        self.create()

    # Build GUI
    def create(self):
        self.root = Tkinter.Tk() # Can be substituted for Toplevel
        self.root.title("Filtered Listbox")

        self.frame = Tkinter.Frame(self.root)
        # I like to use pack because I like the aesthetic feel
        # pady is 5 so that the widgets in the frame are spaced evenly
        self.frame.pack(fill="both", padx=10, pady=5)

        self.filter_mode = Tkinter.StringVar(); # Combobox StringVar
        # Set it to the initial value of combobox
        # Also consider using self.options[0] for uniformity
        self.filter_mode.set("All")

        self.combobox = ttk.Combobox(
            self.frame, textvariable=self.filter_mode, state="readonly",
            values=self.options)
        self.combobox.pack(fill="x", pady=5)

        # So that the scroll bar can be packed nicely
        self.treeview_frame = Tkinter.Frame(self.frame)
        self.treeview_frame.pack(fill="x", pady=5)

        column_headings = ["A", "B", "C"] # These are just examples
        self.treeview = ttk.Treeview(
            self.treeview_frame, columns=column_headings, show="headings")
        self.treeview.pack(fill="y", side="left")

        self.treeview_scroll = ttk.Scrollbar(
            self.treeview_frame, orient="vertical", command=self.treeview.yview)
        self.treeview_scroll.pack(fill="y", side="right")
        self.treeview.config(yscrollcommand=self.treeview_scroll.set)

    # Recursize update function called with root.after
    def update(self):
        filter_mode = self.filter_mode.get()

        # Check for change in the filter_mode
        if filter_mode != self.last_filter_mode:

            items = self.treeview.get_children()
            for item in items:
                self.treeview.delete(item) # Clear the treeview

            # Combobox options
            if filter_mode == "All":
                for element in self.values:
                    self.treeview.insert("", "end", values=(element))

            if filter_mode == "Odd":
                for element in filter(
                    lambda x: True if x % 2 != 0 else False, self.values):
                    self.treeview.insert("", "end", values=(element))

            if filter_mode == "Even":
                for element in filter(
                lambda x: True if x % 2 == 0 else False, self.values):
                    self.treeview.insert("", "end", values=(element))

            self.last_filter_mode = filter_mode # Update current filter mode

        self.root.after(100, self.update) # Call this function again

    def main(self):
        self.update() # Start the recursive update function
        self.root.mainloop() # Start the app

a = App()
a.main()