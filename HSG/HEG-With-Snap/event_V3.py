from events import Events


class Eventmanager():

    def __init__(self, function1,function2):
        self.event1 = Events()
        self.event2 = Events()
        self.func1 = function1
        self.func2 = function2
        self.register()

    def register(self):
        self.event1.on_change += self.func1
        self.event2.on_change += self.func2


    def fire1(self):
        self.handeler = self.event1.on_changes
        if (self.handeler != None):
            self.event1.on_change()

    def fire2(self):
        self.handeler = self.event2.on_changes
        if (self.handeler != None):
            self.event2.on_change()


class event(Eventmanager):
    def __init__(self, function1,function2):
        self.func1 = function1
        self.func2 = function2
        self._x = 0
        self._y = 0
        super().__init__(self.func1,self.func2)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            super().fire1()
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            super().fire2()
            self._y = value


if __name__ == '__main__':

    def exe1(n):
        print(f"number value is {n}")

    def exe2(n):
        print(f"number value is {n}")



    e1 = event(lambda: exe1(10),lambda : exe2(20))

    for i in range(10):
        e1.x = i
        e1.y = i
