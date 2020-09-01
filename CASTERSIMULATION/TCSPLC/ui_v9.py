import datetime
import os
import queue
import logging
import signal
import PIL.Image
import PIL.ImageTk
import alldevices_V3
import general
import allcylinderdprocessing_V1
import allmotor1dprocessing_V1
import allmotor2dprocessing
import allvalve1sprocessing
import allvalve2sprocessing
import allcontrolvalvesprocessing
import allanalogprocessing
import alldigitalprocessing
import time
from ListView2 import *

from clientcomm_v1 import *
import threading
from tkinter import filedialog



from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W, DISABLED, NORMAL

logger = logging.getLogger("main.log")


# print(logger)


class Clock(threading.Thread):
    """Class to display the time every seconds
    Every 5 seconds, the time is displayed using the logging.ERROR level
    to show that different colors are associated to the log levels
    """

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        logger.debug('Simulation started')
        while not self._stop_event.is_set():
            now = datetime.datetime.now()
            # level = logging.INFO
            # logger.log(level, now)
            time.sleep(1)

    def stop(self):
        self._stop_event.set()






class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """
    # Example from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    # (https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget) is not thread safe!
    # See https://stackoverflow.com/questions/43909849/tkinter-python-crashes-on-new-thread-trying-to-log-on-main-thread

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class FormUi:

    def __init__(self, frame,progressbar):
        self.progressbar = progressbar
        self.frame = frame
        self.listofwritetags = []
        self.button1 = ttk.Button(self.frame, text='Connect', command=self.connectwithplc,state=NORMAL)
        self.button1.grid(column=1, row=2, sticky=W,padx=5, pady=5)
        self.button2 = ttk.Button(self.frame, text='Initialization', command=self.initilization,state=DISABLED)
        self.button2.grid(column=1, row=3, sticky=W,padx=5, pady=5)

        self.button3 = ttk.Button(self.frame, text='Start', command=self.startprocess,state =DISABLED)
        self.button3.grid(column=1, row=4, sticky=W,padx=5, pady=5)

        self.button4 = ttk.Button(self.frame, text='Stop', command=self.stopprocess, state=NORMAL)
        self.button4.grid(column=1, row=5, sticky=W, padx=5, pady=5)









    def connectwithplc(self):

        try:

            self.import_file_path = filedialog.askopenfilename()
            self.comm_object = general.General(self.import_file_path)
            self._elementlist = []
            self.tagvalueitemlist = []
            self.plc_cmd_list = []
            self.readsuccess = False

        except Exception as e:
            level = logging.ERROR
            now = datetime.datetime.now()
            messege = "Error is " +str(e) + "from communication function"
            logger.log(level,messege)

            print(e.args)

        finally:
            self.comm_sts = self.comm_object.sta_con_plc
            if self.comm_sts:
                self.button1.config(text="Connected")
                self.button2["state"] = NORMAL
                level = logging.INFO
                messege =  'Event:' + "PLC Simulation Successfully Connected"
                logger.log(level, messege)




    def initilization(self):
        initial = "False"

        self.listofthread =[]
        self.listofprocess = []


        try:


            self.progressbar['value'] = 20
            time.sleep(1)
            self.frame.update_idletasks()
            self.alldevices = alldevices_V3.AllDevices(self.comm_object, self.import_file_path)
            self.progressbar['value'] = 30

            self.frame.update_idletasks()
            time.sleep(1)



            self.allcylinderprocessobject = allcylinderdprocessing_V1.cylinderprocess(self.alldevices,self.import_file_path)
            self.allmotor1dprocessobject = allmotor1dprocessing_V1.motor1dprocess(self.alldevices,self.import_file_path)
            self.motor2dprocessobject = allmotor2dprocessing.motor2dprocess(self.alldevices, self.import_file_path)
            self.sov1sprocessobject = allvalve1sprocessing.sov1sprocess(self.alldevices, self.import_file_path)
            self.sov2sprocessobject = allvalve2sprocessing.sov2sprocess(self.alldevices, self.import_file_path)
            self.controlvalveprocessobject = allcontrolvalvesprocessing.controlvalveprocess(self.alldevices,self.import_file_path)
            self.analogobject = allanalogprocessing.analogprocess(self.alldevices, self.import_file_path)
            self.digitalobject = alldigitalprocessing.digitalprocess(self.alldevices, self.import_file_path)

            self.button2.config(text="Initialized")
            initial = "True"
            self.progressbar['value'] = 100
            self.progressbar.stop()


        except Exception as e:
            initial = "False"
            level = logging.INFO
            messege = 'Event:' + "Initialization Failed"
            logger.log(level, messege)
            logger.exception(e)
            self.progressbar.stop()


        finally:
            if initial:
                self.button3["state"] = NORMAL
            self.progressbar.stop()



    def callcylinder(self,com,devices):
        while not self.DEAD:
            self.allcylinderprocessobject.process()


    def callallmotor1d(self,com,devices):

        while not self.DEAD:
            self.allmotor1dprocessobject.process()


    def callallmotor2d(self,com,devices):

        while not self.DEAD:
            self.motor2dprocessobject.process()
            # allmotor2dprocessing.process(com, devices,self.import_file_path)


    def callallsov1s(self,com,devices):
        while not self.DEAD:
            self.sov1sprocessobject.process()

            # time.sleep(5)

    def callallsov2s(self, com, devices):
        while not self.DEAD:
            self.sov2sprocessobject.process()
            # time.sleep(2)
    #
    def callallanalogs(self,com, devices):
        while not self.DEAD:
            self.analogobject.process()
            # time.sleep(2)


    def callcontrolvalves(self,com,devices):
        while not self.DEAD:
            self.controlvalveprocessobject.process()
            # time.sleep(2)

    def calldigitals(self,com,devices):
        while not self.DEAD:
            self.digitalobject.process()
            # time.sleep(2)



    def cylinderstart(self):
        self.DEAD = False
        self.cylindertread = threading.Thread(target=self.callcylinder, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.cylindertread)
        self.cylindertread.start()
        self.Cylinderbutton.configure(text="Cylinderstarted")


    def motor1dstart(self):
        self.DEAD = False

        self.motor1dtread = threading.Thread(target=self.callallmotor1d, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.motor1dtread)
        self.motor1dtread.start()
        self.motor1dstartbutton.configure(text="motor1dstarted")

    def motor2dstart(self):
        self.DEAD = False
        self.motor2dtread = threading.Thread(target=self.callallmotor2d, args=(self.comm_object, self.alldevices))

        self.motor2dtread.start()
        self.motor2dstartbutton.configure(text="motor2dstarted")

    def sov1start(self):
        self.DEAD = False
        self.sov1stread = threading.Thread(target=self.callallsov1s, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.sov1stread)
        self.sov1stread.start()
        self.sov1startbutton.configure(text="sov1started")

    def sov2start(self):
        self.DEAD = False
        self.sov2stread = threading.Thread(target=self.callallsov2s, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.sov2stread)
        self.sov2stread.start()
        self.sov2startbutton.configure(text="sov2started")

    def analogstart(self):
        self.DEAD = False
        self.analogtread = threading.Thread(target=self.callallanalogs, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.analogtread)
        self.analogtread.start()
        self.analogstartbutton.configure(text="analogstarted")


    def controlvalvestart(self):
        self.DEAD = False
        self.controlvalvetread = threading.Thread(target=self.callcontrolvalves,args=(self.comm_object, self.alldevices))
        self.controlvalvetread.start()
        self.controlvalvestartbutton.configure(text="controlvalvestarted")

    def digitalstart(self):
        self.DEAD = False
        self.digitaltread = threading.Thread(target=self.calldigitals,args=(self.comm_object, self.alldevices))
        self.digitaltread.start()
        self.digitalstartbutton.configure(text="digitalstarted")

    def startprocess(self):

        self.win = tk.Toplevel(self.frame)
        self.win.geometry("500x200")

        self.Cylinderbutton = ttk.Button(self.win, text='CylinderStart', command=self.cylinderstart)
        self.Cylinderbutton.grid(column=0, row=0)

        self.motor1dstartbutton = ttk.Button(self.win, text='motor1dstart', command=self.motor1dstart)
        self.motor1dstartbutton.grid(column=0, row=1)

        self.motor2dstartbutton = ttk.Button(self.win, text='motor2dstart', command=self.motor2dstart)
        self.motor2dstartbutton.grid(column=0, row=2)

        self.sov1startbutton = ttk.Button(self.win, text='sov1start', command=self.sov1start)
        self.sov1startbutton.grid(column=0, row=3)

        self.sov2startbutton = ttk.Button(self.win, text='sov2start', command=self.sov2start)
        self.sov2startbutton.grid(column=0, row=4)


        self.analogstartbutton = ttk.Button(self.win, text='analogstart', command=self.analogstart)
        self.analogstartbutton.grid(column=1, row=1)


        self.controlvalvestartbutton = ttk.Button(self.win, text='controlvalstart', command=self.controlvalvestart)
        self.controlvalvestartbutton.grid(column=1, row=2)

        self.digitalstartbutton = ttk.Button(self.win, text='digitalvalstart', command=self.digitalstart)
        self.digitalstartbutton.grid(column=1, row=3)












    def stopprocess(self):

        self.DEAD = True
        self.Cylinderbutton.configure(text = 'CylinderStart')
        self.motor1dstartbutton.configure(text='motor1dstart')
        self.motor2dstartbutton.configure(text='motor2dstart')
        self.sov1startbutton.configure(text='sov1start')
        self.sov2startbutton.configure(text='sov2start')
        self.controlvalvestartbutton.configure(text='controlvalstart')
        self.analogstartbutton.configure(text='analogstart')






class ThirdUi:

    def __init__(self,frame):
        self.frame = frame
        stim_filename = "smslogo.png"
        # create the PIL image object:
        PIL_image = PIL.Image.open(stim_filename)
        self.img = PIL.ImageTk.PhotoImage(file="smslogo.png")
        label=Label(self.frame, image =self.img)
        label.image = self.img
        Label.anchor=N

        label.pack(side='right')



class App:
    def __init__(self, root):
        self.root = root
        root.title('SMS JSW CASTER DRIVE PLC SIMULATION')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        form_frame = ttk.Labelframe(horizontal_pane, text="Control Panel")
        form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        console_frame = ttk.Labelframe(horizontal_pane, text="Console")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        third_frame = LabelFrame(vertical_pane, text="Third Panel")
        vertical_pane.add(third_frame, weight=1)
        ttk.Label(third_frame, text='Progress Bar').pack(side=LEFT)
        self.progressbar = ttk.Progressbar(third_frame, orient=HORIZONTAL, length=500, mode='determinate')
        self.progressbar.pack(side=LEFT)
        # Initialize all frames
        self.form = FormUi(form_frame,self.progressbar)
        self.console = ConsoleUi(console_frame)
        self.third = ThirdUi(third_frame)
        self.clock = Clock()
        self.clock.start()
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.signal_handler)



    def quit(self, *args):
        self.clock.stop()
        os.system("taskkill /f /im  TCS.exe")
        self.root.destroy()

    def signal_handler(sig, frame):
        print("System exited")
        sys.exit(0)

def main():
    logging.basicConfig(level=logging.DEBUG)

    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


