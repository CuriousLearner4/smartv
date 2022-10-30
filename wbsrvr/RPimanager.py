import time
import multitasking
import serial
#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522

class RPiManager():
    def __init__(self):
        self.user = None
        self.dispensestatus = None
        self.dispenseflag = None
        self.mode = None
        self.quantity = 0
        self.unitprice = 5
        self.payablecoinamount = 0
        self.samplecredits = 25
        self.message = None
        self.message1 = None
    
    def clean_up(self):
        self.user = None
        self.dispensestatus = None
        self.samplecredits = 25
        self.message1 = None
        self.mode = None
        self.payablecoinamount = 0
        self.quantity = 0
        self.message = None
        self.dispenseflag = None
    
    @multitasking.task
    def payment_processor(self):
        if self.mode == "coin":
            self.coin_payment()
        elif self.mode == "rfid":
            self.rfid_payment()
        elif self.mode == "qr":
            self.qr_payment()
    
    def coin_payment(self):
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        now = time.time()
        payable = int(self.quantity)*self.unitprice
        while time.time()-now < 30:
            number = ser.readline()
            if number != b'':
                coin_amount = int.from_bytes(number, byteorder='big')
                self.payablecoinamount += coin_amount
            
    def rfid_payment(self):
        #reader = SimpleMFRC522()
        try:
            flag = False
            now = time.time()
            while (time.time() - now) < 30:
                # id, text = reader.read()
                self.user = 'harsha'
                if self.user != None:
                    flag = True
                    payable = int(self.quantity)*self.unitprice
                    break 
            if flag and self.samplecredits > payable:
                self.samplecredits = self.samplecredits - payable
                self.message = "Hello"+str(self.user)+"!!! Payable: " + str(payable)
                self.message1 = "Your new credits are: " + str(self.samplecredits)
                self.dispenseflag = True
            elif flag and self.samplecredits < payable:
                self.message = "Hello"+str(self.user)+"!!! You have low credits.Try again after TOPUP of card"
                self.dispenseflag = False
        finally:
            pass
            #GPIO.cleanup()
    
    def qr_payment():
        pass

    @multitasking.task
    def pad_dispenser(self):
        # durationofrotation = 0.16666
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(22,GPIO.OUT)
        # GPIO.setup(23,GPIO.OUT)
        # GPIO.setup(24,GPIO.OUT)
        # p = GPIO.PWM(24,1023)
        # try: 
        #     GPIO.output(22,GPIO.HIGH)
        #     GPIO.output(23,GPIO.LOW)
        #     p.start(100)
        #     time.sleep(self.quantity*durationofrotation)
        #     p.stop
        #     self.dispensestatus = "done"
        # except:
        #     self.message = "Something went wrong please contact admin"
        #     self.dispensestatus = "failed"
        # finally:
        #     GPIO.cleanup()
        print('inmotor')
        time.sleep(10)
        self.dispensestatus = 'done'
        