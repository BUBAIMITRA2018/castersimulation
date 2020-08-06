from multiprocessing import Process, Pipe
import threading
import  time




def f(i,name):
    while i <10:
        print('hello', name)
        i = i+1


def execute (i,name) :
    p = threading.Thread(target=f, args=(i,name,))
    p.start()


if __name__ == '__main__':

    class test:
        def __init__(self):
            self.name = " subrata"
            global  i
            i = 0
            self.process(i)

            j = 0
            while j < 10:
                print(" I love mango ")
                j = j+1
                time.sleep(2)

        def process(self,i):
            execute(i,self.name)

    t =test()

    print("increase value i", i)



















