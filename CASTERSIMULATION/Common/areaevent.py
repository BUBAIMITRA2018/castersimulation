from events import Events



class Eventmanager():

    def __init__(self):
        self.events = Events()



    def register(self,func,**args):
      self.events.on_change += func(**args)


    def fire(self):
        self.handeler = self.events.on_changes
        if (self.handeler != None):
            self.events.on_change()


class event(Eventmanager):
    def __init__(self, function):
        self.func = function
        self._x = 0
        super().__init__(self.func)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            super().fire()
            self._x = value


if __name__ == '__main__':

    def exe(n):
        print(f"number value is {n}")


    e1 = event(lambda : exe(10))


    for i in range(10):
        e1.x = i































