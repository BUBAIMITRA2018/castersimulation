import datetime
import queue
import logging
import os
import signal
import multiprocessing
import PIL.Image
import PIL.ImageTk
import AutocompleteCombox
import allmotor1dprocessing_V1
import allmotor2dprocessing
import allvalve1sprocessing
import allvalve2sprocessing
import allencoderprocessing
import allsiemensdriveprocessing
import allcontrolvalvesprocessing
import allanalogprocessing
import alldigitalprocessing
import allabpdriveprocessing
import allrampprocessing
import  allpropotionalvalvesprocessing



import general
import Encoder_Operation_V1
import time
from ListView2 import *
from logger import *
import alldevices_V3
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


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

class process_with_trace(multiprocessing.Process):
    def __init__(self, *args, **keywords):
        multiprocessing.Process.__init__(self, *args, **keywords)
        self.killed = False

        self.queue = multiprocessing.Queue()


    def run(self):
        self.process = multiprocessing.Process.start(self)

    def kill(self):
        self.process.terminate()


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

        self.button5 = ttk.Button(self.frame, text='Force', command=self.force, state=NORMAL)
        self.button5.grid(column=1, row=6, sticky=W, padx=5, pady=5)

        self.button6 = ttk.Button(self.frame, text='ControlPanel', command=self.creatcontrolpanel, state=NORMAL)
        self.button6.grid(column=1, row=7, sticky=W, padx=5, pady=5)

        self.button7 = ttk.Button(self.frame, text='Encoder', command=self.encoderoperation, state=NORMAL)
        self.button7.grid(column=1, row=8, sticky=W, padx=5, pady=5)


    def encoderoperation(self):
        # df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='Encoder')

        Encoder_Operation_V1.Encoder_Operation(self.frame,self.comm_object,self.alldevices )

    def conectionpopup(self):
        self.connect = tk.Toplevel(self.frame)
        self.connect.geometry('400x200')
        ttk.Label(self.connect, text='Browser').grid(column=2, row=0)
        value = StringVar()
        self.excelpath = ttk.Entry(self.connect, width=40, textvariable=value)
        self.excelpath.grid(column=2, row=1)
        self.button1 = ttk.Button(self.connect, text='sumit', command=self.connectwithplc(), state=NORMAL)
        self.button1.grid(column=1, row=2, sticky=W, padx=5, pady=5)

        excelpath = str(self.excelpath.get())
        return excelpath




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
            log_exception(e)
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

            self.listofwritetags = self.collectwritetaglist()
            self.progressbar['value'] = 20
            time.sleep(1)
            self.frame.update_idletasks()
            self.alldevices = alldevices_V3.AllDevices(self.comm_object,self.import_file_path)
            self.progressbar['value'] = 30
            self.frame.update_idletasks()
            time.sleep(1)


            self.allmotor1dprocessobject = allmotor1dprocessing_V1.motor1dprocess(self.alldevices,self.import_file_path)
            self.motor2dprocessobject = allmotor2dprocessing.motor2dprocess(self.alldevices,self.import_file_path)
            self.sov1sprocessobject = allvalve1sprocessing.sov1sprocess(self.alldevices, self.import_file_path)
            self.sov2sprocessobject = allvalve2sprocessing.sov2sprocess(self.alldevices, self.import_file_path)
            self.controlvalveprocessobject = allcontrolvalvesprocessing.controlvalveprocess(self.alldevices,self.import_file_path)
            self.driveobject = allsiemensdriveprocessing.siemensdriveprocessing(self.alldevices,self.import_file_path)
            self.analogobject = allanalogprocessing.analogprocess(self.alldevices,self.import_file_path)
            self.digitalobject = alldigitalprocessing.digitalprocess(self.alldevices,self.import_file_path)
            self.abbobject = allabpdriveprocessing.abpdriveprocessing(self.alldevices,self.import_file_path)
            # self.rampobject = allrampprocessing.rampprocess(self.alldevices,self.import_file_path)
            self.proportionalvalveobject = allpropotionalvalvesprocessing.proportionalvalveprocess(self.alldevices,self.import_file_path)





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


    def callallmotor1d(self,com,devices):

        while not self.DEAD:
            self.allmotor1dprocessobject.process()


    def callallmotor2d(self,com,devices):

        while not self.DEAD:
            self.motor2dprocessobject.process()
            # allmotor2dprocessing.process(com, devices,self.import_file_path)


    def callallsov1s(self,com,devices):
        # self.sov1sreadgeneral = ReadGeneral(com.sta_con_plc)

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

    def callallramps(self, com, devices):
        while not self.DEAD:
            self.rampobject.process()
            # time.sleep(2)


    def callendocers(self,com,devices):
        while not self.DEAD:
            allencoderprocessing.process(com, devices)
            # time.sleep(2)
    #
    # def callallsiemensdrive(self,com,devices):
    #     while not self.DEAD:
    #         self.siemensdriveobject.process()

    def callDrives(self,com,devices):
        while not self.DEAD:
            self.abbobject.process()
            # time.sleep(2)a

    def callcontrolvalves(self,com,devices):
        while not self.DEAD:
            self.controlvalveprocessobject.process()
            # time.sleep(2)

    def calldiigitalprocess(self,com,devices):
        while not self.DEAD:
            self.digitalobject.process()


    def callpropotionalvalveprocess(self,com,deice):
        while not self.DEAD:
            self.proportionalvalveobject.process()




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

    def encoderstart(self):
        self.DEAD = False
        self.encodertread = threading.Thread(target=self.callendocers, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.encodertread)
        self.encodertread.start()
        self.motor1dstartbutton.configure(text="motor1dstarted")

    def analogstart(self):
        self.DEAD = False
        self.analogtread = threading.Thread(target=self.callallanalogs, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.analogtread)
        self.analogtread.start()
        self.analogstartbutton.configure(text="analogstarted")

    def rampstart(self):
        self.DEAD = False
        self.ramptread = threading.Thread(target=self.callallramps, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.ramptread)
        self.ramptread.start()
        self.rampstartbutton.configure(text="rampstarted")

    def abbdrivestart(self):
        self.DEAD = False
        self.abbtread = threading.Thread(target=self.callDrives,
                                              args=(self.comm_object, self.alldevices))
        self.abbtread.start()
        self.drivestartbutton.configure(text="drivestarted")



    # def seimensdrivestart(self):
    #     self.DEAD = False
    #     self.siemnenstread = threading.Thread(target=self.callallsiemensdrive, args=(self.comm_object, self.alldevices))
    #     self.siemnenstread.start()
    #     self.drivestartbutton.configure(text="drivestarted")

    def controlvalvestart(self):
        self.DEAD = False
        self.controlvalvetread = threading.Thread(target=self.callcontrolvalves,args=(self.comm_object, self.alldevices))
        self.controlvalvetread.start()
        self.controlvalvestartbutton.configure(text="controlvalvestarted")

    def digitalprocessstart(self):
        self.DEAD = False
        self.digitaltread = threading.Thread(target=self.calldiigitalprocess, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.digitaltread)
        self.digitaltread.start()
        self.digitalstartbutton.configure(text="digitaltarted")


    def proportionalprocessstart(self):
        self.DEAD = False
        self.proportionalvalvetread = threading.Thread(target=self.callpropotionalvalveprocess, args=(self.comm_object, self.alldevices))
        self.listofthread.append(self.proportionalvalvetread)
        self.proportionalvalvetread.start()
        self.proportionalstartbutton.configure(text="proprotionalvalvestarted")






    def startprocess(self):

        self.win = tk.Toplevel(self.frame)
        self.win.geometry("250x200")

        self.motor1dstartbutton = ttk.Button(self.win, text='motor1dstart', command=self.motor1dstart)
        self.motor1dstartbutton.grid(column=0, row=0)

        self.motor2dstartbutton = ttk.Button(self.win, text='motor2dstart', command=self.motor2dstart)
        self.motor2dstartbutton.grid(column=0, row=1)

        self.sov1startbutton = ttk.Button(self.win, text='sov1start', command=self.sov1start)
        self.sov1startbutton.grid(column=0, row=2)

        self.sov2startbutton = ttk.Button(self.win, text='sov2start', command=self.sov2start)
        self.sov2startbutton.grid(column=0, row=3)

        self.digitalstartbutton = ttk.Button(self.win, text='digital', command=self.digitalprocessstart)
        self.digitalstartbutton.grid(column=0, row=4)

        self.encoderstartbutton = ttk.Button(self.win, text='encoderstart', command=self.encoderstart)
        self.encoderstartbutton.grid(column=1, row=0)

        # self.analogstartbutton = ttk.Button(self.win, text='analogstart', command=self.analogstart)
        # self.analogstartbutton.grid(column=1, row=1)

        self.drivestartbutton = ttk.Button(self.win, text='drivestart', command=self.abbdrivestart)
        self.drivestartbutton.grid(column=1, row=2)

        self.controlvalvestartbutton = ttk.Button(self.win, text='controlvalstart', command=self.controlvalvestart)
        self.controlvalvestartbutton.grid(column=1, row=3)

        # self.rampstartbutton = ttk.Button(self.win, text='rampstart', command=self.rampstart)
        # self.rampstartbutton.grid(column=1, row=4)

        # self.proportionalstartbutton = ttk.Button(self.win, text='ProportionalStart', command=self.proportionalprocessstart)
        # self.proportionalstartbutton.grid(column=0, row=5)


    def stopprocess(self):

        self.DEAD = True
        self.motor1dstartbutton.configure(text = 'motor1dstart')
        self.motor2dstartbutton.configure(text = 'motor2dstart')
        self.sov1startbutton.configure(text = 'sov1start')
        self.sov2startbutton.configure(text = 'sov2start')
        self.encoderstartbutton.configure(text = 'encoderstart')
        self.controlvalvestartbutton.configure(text = 'controlvalstart')
        self.drivestartbutton.configure(text = 'drivestart')
        self.digitalstartbutton.configure(text='digitalstart')
        self.proportionalstartbutton.configure(text='ProportionalStart')






    def writetag(self):
        tagname = self.tagname_entered.get()
        datatype = self.datatype_entered.get()
        tagvalue = int(self.tagvalue.get())
        # tagvalue = 1
        try:


            if len(tagname) >= 3:

                self.comm_object.writegeneral.writesymbolvalue(tagname, tagvalue,datatype)

                level = logging.DEBUG
                messege = tagname + " Force Value is " + str(tagvalue)
                logger.log(level, messege)

        except Exception as e :
            log_exception(e)
            level = logging.ERROR
            messege = "Error is " +str(e) + "from Force function"
            logger.log(level, messege)

    def force(self):
        self.win = tk.Toplevel(self.frame)
        self.win.geometry('300x100')

        self.listofwritetags  =self.collectwritetaglist()
        ttk.Label(self.win,text = 'Choose Tag').grid(column=1,row = 0)
        self.tagname_entered = AutocompleteCombox.AutocompleteCombobox(self.win,width=10)
        self.tagname_entered.grid(column=1,row = 1)

        self.datatype_entered = AutocompleteCombox.AutocompleteCombobox(self.win, width=10)
        self.datatype_entered.grid(column=1, row=2)

        self.tagname_entered.set_completion_list(self.listofwritetags)
        self.datatype_entered.set_completion_list(['S7WLBit','S7WLWord'])
        self.tagname_entered.focus_set()
        self.datatype_entered.focus_set()

        ttk.Label(self.win, text='Enter Value').grid(column=2, row=0)
        value = IntVar()
        self.tagvalue = ttk.Entry(self.win, width=12, textvariable=value)
        self.tagvalue.grid(column=2, row=1)

        ttk.Label(self.win, text='Action').grid(column=2, row=3)
        self.button1 = ttk.Button(self.win, text="Submit", command=self.writetag,state=NORMAL)
        self.button1.grid(column=3, row=3)
        self.win.mainloop()

    def collectwritetaglist(self):
        list1 = []
        df = pd.read_excel(self.import_file_path, sheet_name='WriteGeneral')
        n = 0
        while n < len(df.index):
            list1.append(str(df.iloc[n,0]))
            n = n + 1
        return  list1




    def creatcontrolpanel(self):
        import fn_controlpanel
        fn_controlpanel.Fn_ControlPanel(self.frame,self.import_file_path)


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
        root.title('SMS ESSER PLC SIMULATION')

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
        os.system("taskkill /f /im  LFMain.exe")
        self.root.destroy()

    def signal_handler(sig, frame):
        print("System exited")
        sys.exit(0)

def main():
    logging.basicConfig(level=logging.DEBUG)

    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


