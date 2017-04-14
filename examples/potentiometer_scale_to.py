#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def loop():
    value = board.potentiometer.scale_to(0, 180)
    print("Potentiometer: {}".format(value))
    board.sleep(0.1)

if __name__ == "__main__":
    while True:
        loop()
