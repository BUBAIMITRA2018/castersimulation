import threading
import callallrailswitch
import callallrailswitch1
import callallrailswitch2
import callallrailswitch3
import callallrailswitch4

class AllDevices:

    def __init__(self,import_file_path):
        self.mylock = threading.Lock()


        self.allrailswitchobjects = callallrailswitch.Cal_AllRailSwitch(import_file_path)
        self.allrailswitch1objects = callallrailswitch1.Cal_AllRailSwitch1(import_file_path)
        self.allrailswitch2objects = callallrailswitch2.Cal_AllRailSwitch2(import_file_path)
        self.allrailswitch3objects = callallrailswitch3.Cal_AllRailSwitch3(import_file_path)
        self.allrailswitch4objects = callallrailswitch4.Cal_AllRailSwitch4(import_file_path)


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




