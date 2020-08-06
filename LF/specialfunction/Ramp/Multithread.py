import threading
import time

# global variable x
x = 0



def increment():
    """
    function to increment global variable x
    """
    global x
    x += 1


def thread_task():

    time.sleep((5000))
    increment()
    """
    task for thread
    calls increment function 100000 times.
    """



def string ():
    print("I love mango")


def main_task():
    global x
    # setting global variable x as 0
    x = 0

    # creating threads
    t1 = threading.Thread(target=thread_task)
    # t2 = threading.Thread(target=thread_task)

    # start threads
    t1.start()
    # t2.start()

    # t1.join()




    # wait until threads finish their job

    print("Iteration {0}: x = {1}".format(i, x))


if __name__ == "__main__":
    for i in range(500):
        string()
        main_task()
        print("hello")




