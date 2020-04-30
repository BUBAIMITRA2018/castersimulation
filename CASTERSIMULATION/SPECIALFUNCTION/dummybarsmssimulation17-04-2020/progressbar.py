from tkinter import Button, Tk, HORIZONTAL

from tkinter.ttk import Progressbar
import time


class MonApp(Tk):
    def __init__(self):
        super().__init__()


        bt1 = Button(self, text='Traitement', command=self.traitement)
        bt1.grid()
        self.progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='indeterminate')
        self.progress.grid()
        self.progress.grid_forget()


    def traitement(self):
        self.progress.grid()
        self.progress.start()
        time.sleep(15)
        ## Just like you have many, many code lines...

        self.progress.stop()

if __name__ == '__main__':

    app = MonApp()
    app.mainloop()