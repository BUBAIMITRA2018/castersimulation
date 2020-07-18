import datetime
import queue
import logging
import signal
import PIL.Image
import PIL.ImageTk

import general
import  allencoderprocessing
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
            self.progressbar['value'] = 30
            self.frame.update_idletasks()
            time.sleep(1)



            self.allencoderprocessobject = allencoderprocessing.Allencoderprocess(self.import_file_path)


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


    def callArm1Lift_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.arm1Lift_Encoder_process()

    def callArm2Lift_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.arm2Lift_Encoder_process()

    def callBA01_BWL_Turret_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.bA01_BWL_Turret_Encoder()

    def CalldB_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.dB_Encoder()

    def CallpR_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.pR_Encoder()

    def CalllevellingRollPos_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.lvellingRollPos_Encoder()

    def callshear_Angel_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.shear_Angel_Encoder()

    def callwSD_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.wSD_Encoder()

    def calltDCar1LiftLower_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.tDCar1LiftLower_Encoder()

    def calltDCar2LiftLower_Encoder(self):
        while not self.DEAD:
            self.allencoderprocessobject.tDCar2LiftLower_Encoder()








    def Arm1Lift_Encoderstart(self):
        self.DEAD = False
        self.Arm1Lift_Encodertread = threading.Thread(target=self.callArm1Lift_Encoder)
        self.listofthread.append(self.Arm1Lift_Encodertread)
        self.Arm1Lift_Encodertread.start()
        self.Arm1Lift_Encoderstartbutton.configure(text="Arm1Lift_Encoder_Started")

    def Arm2Lift_Encoderstart(self):
        self.DEAD = False
        self.Arm2Lift_Encodertread = threading.Thread(target=self.callArm2Lift_Encoder)
        self.listofthread.append(self.Arm2Lift_Encodertread)
        self.Arm2Lift_Encodertread.start()
        self.Arm2Lift_Encoderstartbutton.configure(text="Arm2Lift_Encoder_Started")

    def BA01_BWL_Turret_Encoderstart(self):
        self.DEAD = False
        self.BA01_BWL_Turret_Encodertread = threading.Thread(target=self.callBA01_BWL_Turret_Encoder)
        self.listofthread.append(self.BA01_BWL_Turret_Encodertread)
        self.BA01_BWL_Turret_Encodertread.start()
        self.BA01_BWL_Turret_Encoderstartbutton.configure(text="BA01_BWL_Turret_Encoder_Started")

    def dB_Encoderstart(self):
        self.DEAD = False
        self.dB_Encodertread = threading.Thread(target=self.CalldB_Encoder)
        self.listofthread.append(self.dB_Encodertread)
        self.dB_Encodertread.start()
        self.dB_Encoderstartbutton.configure(text="DB_Encoder_Started")

    def pR_Encoderstart(self):
        self.DEAD = False
        self.pR_Encodertread = threading.Thread(target=self.CallpR_Encoder)
        self.listofthread.append(self.pR_Encodertread)
        self.pR_Encodertread.start()
        self.pR_Encoderstartbutton.configure(text="PR_Encoder_Started")

    def shear_Angel_Encoderstart(self):
        self.DEAD = False
        self.shear_Angel_Encodertread = threading.Thread(target=self.callshear_Angel_Encoder)
        self.listofthread.append(self.shear_Angel_Encodertread)
        self.shear_Angel_Encodertread.start()
        self.shear_Angel_Encoderstartbutton.configure(text="Shear_Angel_Encoder_Started")


    def wSD_Encoderstart(self):
        self.DEAD = False
        self.wSD_Encodertread = threading.Thread(target=self.callwSD_Encoder)
        self.listofthread.append(self.wSD_Encodertread)
        self.wSD_Encodertread.start()
        self.wSD_Encoderstartbutton.configure(text="WSD_Encoder_Started")

    def tDCar1LiftLower_Encoderstart(self):
        self.DEAD = False
        self.tDCar1LiftLower_Encodertread = threading.Thread(target=self.calltDCar1LiftLower_Encoder)
        self.listofthread.append(self.tDCar1LiftLower_Encodertread)
        self.tDCar1LiftLower_Encodertread.start()
        self.tDCar1LiftLower_Encoderstartbutton.configure(text="TDCar1LiftLower_Encoder_Started")

    def tDCar2LiftLower_Encoderstart(self):
        self.DEAD = False
        self.tDCar2LiftLower_Encodertread = threading.Thread(target=self.calltDCar2LiftLower_Encoder)
        self.listofthread.append(self.tDCar2LiftLower_Encodertread)
        self.tDCar2LiftLower_Encodertread.start()
        self.tDCar2LiftLower_Encoderstartbutton.configure(text="TDCar2LiftLower_Encoder_Started")

    def levellingRollPos_Encoderstart(self):
        self.DEAD = False
        self.levellingRollPos_Encodertread = threading.Thread(target=self.CalllevellingRollPos_Encoder)
        self.listofthread.append(self.levellingRollPos_Encodertread)
        self.levellingRollPos_Encodertread.start()
        self.levellingRollPos_Encoderstartbutton.configure(text="LevellingRollPos_Encoder_Started")



    def startprocess(self):

        self.win = tk.Toplevel(self.frame)
        self.win.geometry("500x200")

        self.Arm1Lift_Encoderstartbutton = ttk.Button(self.win, text='Arm1Lift_Encoder_Start', command=self.Arm1Lift_Encoderstart)
        self.Arm1Lift_Encoderstartbutton.grid(column=0, row=0)

        self.Arm2Lift_Encoderstartbutton = ttk.Button(self.win, text='Arm2Lift_Encoder_Start', command=self.Arm2Lift_Encoderstart)
        self.Arm2Lift_Encoderstartbutton.grid(column=1, row=0)

        self.BA01_BWL_Turret_Encoderstartbutton = ttk.Button(self.win, text='BA01_BWL_Turret_Encoder_Start',
                                                      command=self.BA01_BWL_Turret_Encoderstart)
        self.BA01_BWL_Turret_Encoderstartbutton.grid(column=0, row=1)

        self.dB_Encoderstartbutton = ttk.Button(self.win, text='DB_Encoder_Start',
                                                             command=self.dB_Encoderstart)
        self.dB_Encoderstartbutton.grid(column=1, row=1)

        self.pR_Encoderstartbutton = ttk.Button(self.win, text='PR_Encoder_Start',
                                                command=self.pR_Encoderstart)
        self.pR_Encoderstartbutton.grid(column=0, row=2)

        self.shear_Angel_Encoderstartbutton = ttk.Button(self.win, text='Shear_Angel_Encoder_Start',
                                                command=self.shear_Angel_Encoderstart)
        self.shear_Angel_Encoderstartbutton.grid(column=1, row=2)

        self.wSD_Encoderstartbutton = ttk.Button(self.win, text='wSD_Encoder_start',
                                                         command=self.wSD_Encoderstart)
        self.wSD_Encoderstartbutton.grid(column=0, row=3)


        self.tDCar1LiftLower_Encoderstartbutton = ttk.Button(self.win, text='TDCar1LiftLower_Encoder_start',
                                                 command=self.tDCar1LiftLower_Encoderstart)
        self.tDCar1LiftLower_Encoderstartbutton.grid(column=1, row=3)

        self.tDCar2LiftLower_Encoderstartbutton = ttk.Button(self.win, text='TDCar2LiftLower_Encoder_start',
                                                             command=self.tDCar2LiftLower_Encoderstart)
        self.tDCar2LiftLower_Encoderstartbutton.grid(column=0, row=4)

        self.levellingRollPos_Encoderstartbutton = ttk.Button(self.win, text='LevellingRollPos_Encoder_start',
                                                             command=self.levellingRollPos_Encoderstart)
        self.levellingRollPos_Encoderstartbutton.grid(column=0, row=4)







    def stopprocess(self):

        self.DEAD = True
        self.Arm1Lift_Encoderstartbutton.configure(text = 'Arm1Lift_Encoder_Start')
        self.Arm2Lift_Encoderstartbutton.configure(text='Arm2Lift_Encoder_Start')
        self.BA01_BWL_Turret_Encoderstartbutton.configure(text='BA01_BWL_Turret_Encoder_Start')
        self.dB_Encoderstartbutton.configure(text='DB_Encoder_Start')
        self.pR_Encoderstartbutton.configure(text='PR_Encoder_Start')
        self.shear_Angel_Encoderstartbutton.configure(text='Shear_Angel_Encoder_Start')
        self.wSD_Encoderstartbutton.configure(text='WSD_Encoder_start')
        self.tDCar1LiftLower_Encoderstartbutton.configure(text='TDCar1LiftLower_Encoder_start')
        self.tDCar2LiftLower_Encoderstartbutton.configure(text='TDCar2LiftLower_Encoder_start')
        self.levellingRollPos_Encoderstartbutton.configure(text='LevellingRollPos_Encoder_start')





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
        self.root.destroy()

    def signal_handler(sig, frame):
        print("System exited")
        sys.exit(0)

def main():
    logging.basicConfig(level=logging.DEBUG)

    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


