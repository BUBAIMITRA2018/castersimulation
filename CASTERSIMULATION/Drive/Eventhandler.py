class EventManager:

    class Event:
        def __init__(self,functions):
            if type(functions) is not list:
                raise ValueError("functions parameter has to be a list")
            self.functions = functions

        def __iadd__(self,func):
            self.functions.append(func)
            return self

        def __isub__(self,func):
            self.functions.remove(func)
            return self

        def __call__(self,*args,**kvargs):
            for func in self.functions : func(*args,**kvargs)

    @classmethod
    def addEvent(cls,**kvargs):
        """
        addEvent( event1 = [f1,f2,...], event2 = [g1,g2,...], ... )
        creates events using **kvargs to create any number of events. Each event recieves a list of functions,
        where every function in the list recieves the same parameters.

        Example:

        def hello(): print "Hello ",
        def world(): print "World"

        EventManager.addEvent( salute = [hello] )
        EventManager.salute += world

        EventManager.salute()

        Output:
        Hello World
        """
        for key in kvargs.keys():
            if type(kvargs[key]) is not list:
                raise ValueError("value has to be a list")
            else:
                kvargs[key] = cls.Event(kvargs[key])

        cls.__dict__.update(kvargs)