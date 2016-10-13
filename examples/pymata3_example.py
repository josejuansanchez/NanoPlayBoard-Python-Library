from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import time

pot_value = {}
ldr_value = {}


def potentiometer_callback(data):
    global pot_value
    pin = data[0]
    pot_value[pin] = (data[1])


def ldr_callback(data):
    global ldr_value
    pin = data[0]
    ldr_value[pin] = (data[1])

board = PyMata3()
board.set_pin_mode(7, Constants.ANALOG, potentiometer_callback)
board.set_pin_mode(6, Constants.ANALOG, ldr_callback)

while True:
    print(pot_value)
    print(ldr_value)
    board.sleep(0.5)
