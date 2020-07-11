import callLTC1

class AllDevices:

    def __init__(self,import_file_path):



        self.LTC1objects = callLTC1.Cal_LTC1(import_file_path)



    @property
    def CallTC1(self):
        return self.LTC1objects





