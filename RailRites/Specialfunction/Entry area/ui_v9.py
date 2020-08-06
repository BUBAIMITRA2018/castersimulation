import datetime
import queue
import logging
import signal
import multiprocessing
import PIL.Image
import PIL.ImageTk
import AutocompleteCombox
import railswitchprocessing
import railswitch1processing
import railswitch2processing
import railswitch3processing
import railswitch4processing
import railswitch5processing
import railswitch6processing
import railswitch7processing
import railswitch8processing
import general
import time
import alldevices_V3
from clientcomm_v1 import *
import threading
from tkinter import filedialog, LEFT
import tkinter as tk



from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W, DISABLED, NORMAL

logger = logging.getLogger("main.log")
print(logger)


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

            # else:
            #     level = logging.ERROR
            #     messege = 'Event:' + "Wrong Excel Confriguation"
            #     logger.log(level, messege)




    def initilization(self):
        initial = "False"

        self.listofthread =[]
        self.listofprocess = []


        try:

            self.listofwritetags = self.collectwritetaglist()
            self.progressbar['value'] = 20
            time.sleep(1)
            self.frame.update_idletasks()
            self.alldevices = alldevices_V3.AllDevices(self.import_file_path)
            self.progressbar['value'] = 30
            self.frame.update_idletasks()
            time.sleep(1)

            self.railswitchobject = railswitchprocessing.railswitchProcess(self.alldevices)
            self.railswitch1object = railswitch1processing.railswitchProcess1(self.alldevices)
            self.railswitch2object = railswitch2processing.railswitchProcess2(self.alldevices)
            self.railswitch3object = railswitch3processing.railswitchProcess3(self.alldevices)
            self.railswitch4object = railswitch4processing.railswitchProcess4(self.alldevices)
            self.railswitch5object = railswitch5processing.railswitchProcess5(self.alldevices)
            self.railswitch6object = railswitch6processing.railswitchProcess6(self.alldevices)
            self.railswitch7object = railswitch7processing.railswitchProcess7(self.alldevices)
            self.railswitch8object = railswitch8processing.railswitchProcess8(self.alldevices)

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




    def callrailswitchs(self):
        while not self.DEAD:
            self.railswitchobject.process()
            time.sleep(2)

    def callrailswitchs1(self):
        while not self.DEAD:
            self.railswitch1object.process()
            time.sleep(2)

    def callrailswitchs2(self):
        while not self.DEAD:
            self.railswitch2object.process()
            time.sleep(2)

    def callrailswitchs3(self):
        while not self.DEAD:
            self.railswitch3object.process()
            time.sleep(2)

    def callrailswitchs4(self):
        while not self.DEAD:
            self.railswitch4object.process()
            time.sleep(2)

    def callrailswitchs5(self):
        while not self.DEAD:
            self.railswitch5object.process()
            time.sleep(2)

    def callrailswitchs6(self):
        while not self.DEAD:
            self.railswitch6object.process()
            time.sleep(2)

    def callrailswitchs7(self):
        while not self.DEAD:
            self.railswitch7object.process()
            time.sleep(2)

    def callrailswitchs8(self):
        while not self.DEAD:
            self.railswitch8object.process()
            time.sleep(2)

    def railswitchstart(self):
        self.DEAD = False
        self.railswitchtread = threading.Thread(target=self.callrailswitchs)
        self.railswitchtread.start()
        self.railswitchstartbutton.configure(text="railswitchstarted")

    def railswitch1start(self):
        self.DEAD = False
        self.railswitch1tread = threading.Thread(target=self.callrailswitchs1)
        self.railswitch1tread.start()
        self.railswitch1startbutton.configure(text="railswitch1started")

    def railswitch2start(self):
        self.DEAD = False
        self.railswitch2tread = threading.Thread(target=self.callrailswitchs2)
        self.railswitch2tread.start()
        self.railswitch2startbutton.configure(text="railswitch2started")

    def railswitch3start(self):
        self.DEAD = False
        self.railswitch3tread = threading.Thread(target=self.callrailswitchs3)
        self.railswitch3tread.start()
        self.railswitch3startbutton.configure(text="railswitch2started")

    def railswitch4start(self):
        self.DEAD = False
        self.railswitch4tread = threading.Thread(target=self.callrailswitchs4)
        self.railswitch4tread.start()
        self.railswitch4startbutton.configure(text="railswitch4started")

    def railswitch5start(self):
        self.DEAD = False
        self.railswitch5tread = threading.Thread(target=self.callrailswitchs5)
        self.railswitch5tread.start()
        self.railswitch5startbutton.configure(text="railswitch5started")

    def railswitch6start(self):
        self.DEAD = False
        self.railswitch6tread = threading.Thread(target=self.callrailswitchs6)
        self.railswitch6tread.start()
        self.railswitch6startbutton.configure(text="railswitch6started")

    def railswitch7start(self):
        self.DEAD = False
        self.railswitch7tread = threading.Thread(target=self.callrailswitchs7)
        self.railswitch7tread.start()
        self.railswitch7startbutton.configure(text="railswitch7started")

    def railswitch8start(self):
        self.DEAD = False
        self.railswitch8tread = threading.Thread(target=self.callrailswitchs8)
        self.railswitch8tread.start()
        self.railswitch8startbutton.configure(text="rollertablestarted")











    def startprocess(self):

        self.win = tk.Toplevel(self.frame)
        self.win.geometry("250x200")


        self.railswitchstartbutton = ttk.Button(self.win, text='railswitchstart', command=self.railswitchstart)
        self.railswitchstartbutton.grid(column=0, row=0)
        self.railswitch1startbutton = ttk.Button(self.win, text='railswitch1start', command=self.railswitch1start)
        self.railswitch1startbutton.grid(column=0, row=1)
        self.railswitch2startbutton = ttk.Button(self.win, text='railswitch2start', command=self.railswitch2start)
        self.railswitch2startbutton.grid(column=0, row=2)
        self.railswitch3startbutton = ttk.Button(self.win, text='railswitch3start', command=self.railswitch3start)
        self.railswitch3startbutton.grid(column=0, row=3)
        self.railswitch4startbutton = ttk.Button(self.win, text='railswitch4start', command=self.railswitch4start)
        self.railswitch4startbutton.grid(column=1, row=0)
        self.railswitch5startbutton = ttk.Button(self.win, text='railswitch5start', command=self.railswitch5start)
        self.railswitch5startbutton.grid(column=1, row=1)
        self.railswitch6startbutton = ttk.Button(self.win, text='railswitch6start', command=self.railswitch6start)
        self.railswitch6startbutton.grid(column=1, row=2)
        self.railswitch7startbutton = ttk.Button(self.win, text='railswitch7start', command=self.railswitch7start)
        self.railswitch7startbutton.grid(column=1, row=3)
        self.railswitch8startbutton = ttk.Button(self.win, text='rollertablestart', command=self.railswitch8start)
        self.railswitch8startbutton.grid(column=1, row=4)


    def stopprocess(self):

        self.DEAD = True
        self.railswitchstartbutton.configure(text='railswitchstart')
        self.railswitch1startbutton.configure(text='railswitch1start')
        self.railswitch2startbutton.configure(text='railswitch2start')
        self.railswitch3startbutton.configure(text='railswitch3start')
        self.railswitch4startbutton.configure(text='railswitch4start')
        self.railswitch5startbutton.configure(text='railswitch5start')
        self.railswitch6startbutton.configure(text='railswitch6start')
        self.railswitch7startbutton.configure(text='railswitch7start')
        self.railswitch8startbutton.configure(text='rollertablestart')

        # for item in self.listofprocess:
        #     item.kill()


    def writetag(self):
        tagname = self.tagname_entered.get()
        datatype = self.datatype_entered.get()
        tagvalue = int(self.tagvalue.get())
        # tagvalue = 1
        try:


            if len(tagname) > 3:
                print("length is",len(str(tagname)))
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
        df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='WriteGeneral')
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
        label= tk.Label(self.frame, image =self.img)
        label.image = self.img
        tk.Label.anchor=N

        label.pack(side='right')



class App:
    def __init__(self, root):
        self.root = root
        root.title('SMS SIMULATION')

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
        third_frame = tk.LabelFrame(vertical_pane, text="Third Panel")
        vertical_pane.add(third_frame, weight=1)
        ttk.Label(third_frame, text='Progress Bar').pack(side=tk.LEFT)
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
        os.system("taskkill /f /im  entryarea.exe")
        self.root.destroy()

    def signal_handler(sig, frame):
        print("System exited")
        sys.exit(0)

def main():
    logging.basicConfig(level=logging.DEBUG)
    df = pd.read_excel(r'C:\OPCUA\Working_VF1_5.xls', sheet_name='Tag List')
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


