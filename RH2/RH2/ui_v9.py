import datetime
import queue
import signal
import multiprocessing
import PIL.Image
import PIL.ImageTk
import AutocompleteCombox
import allvalve1sprocessing
import allmotor1dprocessing_V1
import  allvalve2sprocessing
import  allmotor2dprocessing
import  allvibrofeedersprocessing
import  allconveyorprocessing
import alldigitalprocessing
import allanalogprocessing
import os
import allcontrolvalvesprocessing
import  allsiemensdriveprocessing
import  allconveyor2dprocessing
import general
import Encoder_Operation_V1
import time
from ListView2 import *
from logger import *
import alldevices_V3
from clientcomm_v1 import *
import threading
from tkinter import filedialog
import json




from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W, DISABLED, NORMAL

logger = logging.getLogger("main.log")



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


        self.button6 = ttk.Button(self.frame, text='Snap', command=self.snap, state=NORMAL)
        self.button6.grid(column=1, row=7, sticky=W, padx=5, pady=5)

        self.button7 = ttk.Button(self.frame, text='SnapUpload', command=self.snapupload, state=NORMAL)
        self.button7.grid(column=1, row=8, sticky=W, padx=5, pady=5)

    def snap(self):
        self.directory = filedialog.askdirectory()
        global format, data_type1
        print(self.import_file_path)
        data = pd.read_excel(self.import_file_path, sheet_name="AnalogTx")
        row, col = data.shape
        dict = {}
        p = 0
        while p < row:
            tag_value = self.comm_object.readgeneral.readsymbolvalue(data.iloc[p, 8], 'S7WLWord', "PE")
            keyvalue = {"AI" + str(data.iloc[p, 8]): tag_value}
            dict.update(keyvalue)
            p = p + 1

        data = pd.read_excel(self.import_file_path, sheet_name="OutputTx")
        row, col = data.shape
        p = 0
        while p < row:
            tag_value = self.comm_object.readgeneral.readsymbolvalue(data.iloc[p, 3], 'S7WLBit', "PE")
            keyvalue = {"DI" + str(data.iloc[p, 3]): tag_value}
            dict.update(keyvalue)
            p = p + 1
        with open(
                self.directory + '\snap' + str(datetime.datetime.now()).replace(" ", "_").replace(".", "_").replace(
                    ":", "_") + '.txt', 'w') as json_file:
            json.dump(dict, json_file)

    def snapupload(self):
        self.import_file_path1 = filedialog.askopenfilename()
        with open(self.import_file_path1) as json_file:
            w = json.load(json_file)
            for item in w:
                if item[0:2] == "DI":
                    format = "PE"
                    data_type1 = 'S7WLBit'
                elif item[0:2] == "AI":
                    format = "PE"
                    data_type1 = 'S7WLWord'

                self.comm_object.writegeneral.writesymbolvalue(item[2::], w[item], data_type1)

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

            self.sov1sprocessobject = allvalve1sprocessing.sov1sprocess(self.alldevices, self.import_file_path)
            self.motor1dprocessobject = allmotor1dprocessing_V1.motor1dprocess(self.alldevices,self.import_file_path)
            self.sov2sprocessobject = allvalve2sprocessing.sov2sprocess(self.alldevices,self.import_file_path)
            self.motor2dprocessobject = allmotor2dprocessing.motor2dprocess(self.alldevices,self.import_file_path)
            self.allvibrofeederobject = allvibrofeedersprocessing.vibrofeederprocess(self.alldevices,self.import_file_path)
            self.allconveyorobject = allconveyorprocessing.allconveyorprocess(self.alldevices, self.import_file_path)
            # self.allanalogobject = allanalogprocessing.analogprocess(self.alldevices, self.import_file_path)
            self.allcontrolvalveobject = allcontrolvalvesprocessing.controlvalveprocess(self.alldevices,self.import_file_path)
            self.alldigitalobject = alldigitalprocessing.digitalprocess(self.alldevices,self.import_file_path)
            self.allsiemendriveobject = allsiemensdriveprocessing.siemensdriveprocessing(self.alldevices,self.import_file_path)
            self.allconveyorobject = allconveyor2dprocessing.conveyor2dprocess(self.alldevices,self.import_file_path)


            self.progressbar['value'] = 50
            self.frame.update_idletasks()
            time.sleep(1)



            # Multithreading section


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





    def callallsov1s(self):
        while TRUE:
            self.sov1sprocessobject.process()


    def callallmotor1d(self):
        while TRUE:
            self.motor1dprocessobject.process()


    def callallsov2s(self):
        while TRUE:
            self.sov2sprocessobject.process()

    def callallmotor2d(self):
        while TRUE:
            self.motor2dprocessobject.process()

    def callallvibrofeeder(self):
        while TRUE:
            self.allvibrofeederobject.process()

    def callallconveyor(self):
        while TRUE:
            self.allconveyorobject.process()

    # def callallanalog(self):
    #     while TRUE:
    #         self.allanalogobject.process()


    def callallramp(self):
        while TRUE:
            self.allrampobjects.process()

    def callallcontrolvalve(self):
        while TRUE:
            self.allcontrolvalveobject.process()

    def callalldigital(self):
        while TRUE:
            self.alldigitalobject.process()

    def callallsiemensdrive(self):
        while TRUE:
            self.allsiemendriveobject.process()

    def callallconveyor2d(self):
        while TRUE:
            self.allconveyorobject.process()



    #
    def sov1start(self):
        self.DEAD = False
        self.sov1stread = threading.Thread(target=self.callallsov1s)
        self.listofthread.append(self.sov1stread)
        self.sov1stread.start()
        self.sov1startbutton.configure(text="Sov1sstarted")
    #

    #
    def motor1dstart(self):
        self.DEAD = False
        self.motor1dtread = threading.Thread(target=self.callallmotor1d)
        self.listofthread.append(self.motor1dtread)
        self.motor1dtread.start()
        self.motor1dstartbutton.configure(text="Motor1dstarted")

    #

    #
    def motor2dstart(self):
        self.DEAD = False
        self.motor2dtread = threading.Thread(target=self.callallmotor2d)
        self.listofthread.append(self.motor2dtread)
        self.motor2dtread.start()
        self.motor2dstartbutton.configure(text="Motor2dstarted")
        #


    #
    def sov2sstart(self):
        self.DEAD = False
        self.sov2stread = threading.Thread(target=self.callallsov2s)
        self.listofthread.append(self.sov2stread)
        self.sov2stread.start()
        self.sov2sstartbutton.configure(text="Sov2sstarted")

    #

    #
    def vibrofeedersstart(self):
        self.DEAD = False
        self.vibrofeedertread = threading.Thread(target=self.callallvibrofeeder)
        self.listofthread.append(self.vibrofeedertread)
        self.vibrofeedertread.start()
        self.vibrofeederstartbutton.configure(text="VibrofeederStarted")

    #

    #
    def conveyorstart(self):
        self.DEAD = False
        self.conveyortread = threading.Thread(target=self.callallconveyor)
        self.listofthread.append(self.conveyortread)
        self.conveyortread.start()
        self.conveyorstartbutton.configure(text="Conveyor1dStarted")

    # def analogstart(self):
    #     self.DEAD = False
    #     self.analogtread = threading.Thread(target=self.callallanalog)
    #     self.listofthread.append(self.analogtread)
    #     self.analogtread.start()
    #     self.analogstartbutton.config(text = 'AnalogStarted')


    def contolvalvestart(self):
        self.DEAD = False
        self.controlvalvetread = threading.Thread(target=self.callallcontrolvalve)
        self.listofthread.append(self.controlvalvetread)
        self.controlvalvetread.start()
        self.controlvalvestartbutton.configure(text="ControlValveStarted")

    #

    def digitalstart(self):
        self.DEAD = False
        self.digitalinputtread = threading.Thread(target=self.callalldigital)
        self.listofthread.append(self.digitalinputtread)
        self.digitalinputtread.start()
        self.digitalstartbutton.config(text = 'DigitalStarted')

    #

    def siemendrivestart(self):
        self.DEAD = False
        self.siemensdrivetread = threading.Thread(target=self.callallsiemensdrive)
        self.listofthread.append(self.siemensdrivetread)
        self.siemensdrivetread.start()
        self.siemensdrivestartbutton.config(text='SiemenDriveStarted')
    #

    def conveyor2dstart(self):
        self.DEAD = False
        self.conveyor2dtread = threading.Thread(target=self.callallconveyor2d)
        self.listofthread.append(self.conveyor2dtread)
        self.conveyor2dtread.start()
        self.conveyor2dstartbutton.config(text='Controlvalve2DStarted')

    def rampstart(self):
        self.DEAD = False
        self.ramptread = threading.Thread(target=self.callallramp)
        self.listofthread.append(self.ramptread)
        self.ramptread.start()
        self.rampstartbutton.config(text='RampStarted')

    #






    def startprocess(self):

        self.win = tk.Toplevel(self.frame)
        self.win.geometry("250x200")

        self.sov1startbutton = ttk.Button(self.win, text='Sov1_Start', command=self.sov1start)
        self.sov1startbutton.grid(column=0, row=0)

        self.motor1dstartbutton = ttk.Button(self.win, text='Motor1d_Start', command=self.motor1dstart)
        self.motor1dstartbutton.grid(column=0, row=1)

        self.sov2sstartbutton = ttk.Button(self.win, text='Sov2s_Start', command=self.sov2sstart)
        self.sov2sstartbutton.grid(column=0, row=2)

        self.motor2dstartbutton = ttk.Button(self.win, text='Motor2d_Start', command=self.motor2dstart)
        self.motor2dstartbutton.grid(column=0, row=3)

        self.vibrofeederstartbutton = ttk.Button(self.win, text='VF_Start', command=self.vibrofeedersstart)
        self.vibrofeederstartbutton.grid(column=1, row=0)

        self.conveyorstartbutton = ttk.Button(self.win, text='Conveyor1d_Start', command=self.conveyorstart)
        self.conveyorstartbutton.grid(column=1, row=1)

        # self.analogstartbutton = ttk.Button(self.win, text='Analog_Start', command=self.analogstart)
        # self.analogstartbutton.grid(column=1, row=2)

        self.controlvalvestartbutton = ttk.Button(self.win, text='Controlvalve_Start', command=self.contolvalvestart)
        self.controlvalvestartbutton.grid(column=1, row=3)

        self.digitalstartbutton = ttk.Button(self.win, text='Digitalinput_Start', command=self.digitalstart)
        self.digitalstartbutton.grid(column=0, row=4)

        self.siemensdrivestartbutton = ttk.Button(self.win, text='SiemensDrive_Start', command=self.siemendrivestart)
        self.siemensdrivestartbutton.grid(column=1, row=4)

        self.conveyor2dstartbutton = ttk.Button(self.win, text='Conveyor2D_Start', command=self.conveyor2dstart)
        self.conveyor2dstartbutton.grid(column=1, row=5)

        # self.rampstartbutton = ttk.Button(self.win, text='Ramp_Start', command=self.rampstart)
        # self.rampstartbutton.grid(column=0, row=5)










    def stopprocess(self):
        self.DEAD = True
        self.motor1dstartbutton.configure(text='Motor1dStart')
        self.motor2dstartbutton.configure(text='Motor2dStart')
        self.sov1startbutton.configure(text='Sov1Start')
        self.sov2sstartbutton.configure(text='Sov2Start')
        self.controlvalvestartbutton.configure(text='ControlvalStart')
        # self.analogstartbutton.configure(text='AnalogStart')
        self.siemensdrivestartbutton.configure(text='SiemendriveStart')
        self.digitalstartbutton.configure(text='DigitalStart')
        self.conveyorstartbutton.config(text = 'Conveyor1dStart')
        self.vibrofeederstartbutton.config(text = 'VibrofeederStart')
        self.conveyor2dstartbutton.config(text = 'Conveyor2dStrat')
        self.rampstartbutton.configure(text = 'RampStart')




    def writetag(self):

        tagname = self.tagname_entered.get()
        datatype = self.datatype_entered.get()
        tagvalue = int(self.tagvalue.get())
        # tagvalue = 1
        try:


            if len(tagname) > 3:

                self.comm_object.writegeneral.writesymbolvalue(tagname,datatype, tagvalue)
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
        self.datatype_entered.set_completion_list(['digital','analog'])
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
        root.title('SMS JSW RH2 SIMULATION')

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
        os.system("taskkill /f /im  RHMain.exe")
        self.root.destroy()

    def signal_handler(sig, frame):
        print("System exited")
        sys.exit(0)





def main():
    logging.basicConfig(level=logging.DEBUG)

    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


