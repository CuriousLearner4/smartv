import time
import serial
import random
import multitasking
class control():
    def __init__(self):
        self.status = None
    @multitasking.task
    def paychk(self,mode):
        if mode == 'coin':
            time.sleep(10)
            self.status = 's'
        else:
            self.status = 'q'
