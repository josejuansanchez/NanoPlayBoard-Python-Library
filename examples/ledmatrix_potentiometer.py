#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def loop():
    value = board.potentiometer.scale_to(0, 99)
    print("Potentiometer: {}".format(value))
    board.ledmatrix.print_number(value)
    board.sleep(0.010)

while True:
    loop()