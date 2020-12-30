from server import startS
from client import start
from _thread import *
import time

num = 1
try:

    start_new_thread(startS, (num,))
    time.sleep(1)
    start_new_thread(start, (num,))
    start_new_thread(start, (num,))
    time.sleep(25)
except:
    print("unable to open thred")

while 1:
    time.sleep(1)
    pass