

class device:
    def __init__(self,n,type):
        self.n = n
        self.type = type

    def process(self):
        for i in range(self.n):
            print(f"hi,{self.type} device created sucessfully")


class allmotor:
    def __init__(self, n):
        self.motors = []
        self.n = n
        for i in range(self.n):
            b = device(i, "motor")
            self.motors.append(b)

    def process(self):
        for i in range(self.n):
            self.motors[i].process()
            print(self.motors[i])




class allsov:
    def __init__(self,n):
        self.sovs = []
        self.n = n
        for i in range(self.n):
            b = device(i,"sov")
            self.sovs.append(b)

    def process(self):
        for i in range(self.n):
            self.sovs[i].process()
            print(self.sovs[i])



class alldevices():
    def __init__(self,n):
        self.motors = allmotor(n)
        self.sovs = allsov(n)

    @property
    def getallmotors(self):
        return self.motors

    @property
    def getallsovs(self):
        return self.sovs






























