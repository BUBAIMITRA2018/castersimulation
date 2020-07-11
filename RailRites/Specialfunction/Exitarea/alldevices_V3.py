import threading
import callallrailswitch
import callallrailswitch1
import callallrailswitch2
import callallrailswitch3
import callallrailswitch4
import callallrailswitch5
import callallrailswitch6
import callallrailswitch7
import callallrailswitch8
import callallrailswitch9
import callallrailswitch10
import callallrailswitch11
import callallrailswitch12
class AllDevices:

    def __init__(self,import_file_path):
        self.mylock = threading.Lock()


        self.allrailswitchobjects = callallrailswitch.Cal_AllRailSwitch(import_file_path)
        self.allrailswitch1objects = callallrailswitch1.Cal_AllRailSwitch1(import_file_path)
        self.allrailswitch2objects = callallrailswitch2.Cal_AllRailSwitch2(import_file_path)
        self.allrailswitch3objects = callallrailswitch3.Cal_AllRailSwitch3(import_file_path)
        self.allrailswitch4objects = callallrailswitch4.Cal_AllRailSwitch4(import_file_path)
        self.allrailswitch5objects = callallrailswitch5.Cal_AllRailSwitch5(import_file_path)
        self.allrailswitch6objects = callallrailswitch6.Cal_AllRailSwitch6(import_file_path)
        self.allrailswitch7objects = callallrailswitch7.Cal_AllRailSwitch7(import_file_path)
        self.allrailswitch8objects = callallrailswitch8.Cal_AllRailSwitch8(import_file_path)
        self.allrailswitch9objects = callallrailswitch9.Cal_AllRailSwitch9(import_file_path)
        self.allrailswitch10objects = callallrailswitch10.Cal_AllRailSwitch10(import_file_path)
        self.allrailswitch11objects = callallrailswitch11.Cal_AllRailSwitch11(import_file_path)
        self.allrailswitch12objects = callallrailswitch12.Cal_AllRailSwitch12(import_file_path)


    @property
    def allrailswitch(self):
        return self.allrailswitchobjects

    @property
    def allrailswitch1(self):
        return self.allrailswitch1objects

    @property
    def allrailswitch2(self):
        return self.allrailswitch2objects

    @property
    def allrailswitch3(self):
        return self.allrailswitch3objects

    @property
    def allrailswitch4(self):
        return self.allrailswitch4objects

    @property
    def allrailswitch5(self):
        return self.allrailswitch5objects

    @property
    def allrailswitch6(self):
        return self.allrailswitch6objects

    @property
    def allrailswitch7(self):
        return self.allrailswitch7objects

    @property
    def allrailswitch8(self):
        return self.allrailswitch8objects

    @property
    def allrailswitch9(self):
        return self.allrailswitch9objects

    @property
    def allrailswitch10(self):
        return self.allrailswitch10objects

    @property
    def allrailswitch11(self):
        return self.allrailswitch11objects

    @property
    def allrailswitch12(self):
        return self.allrailswitch12objects




