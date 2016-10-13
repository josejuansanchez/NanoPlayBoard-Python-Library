#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def read_callback(data):
    print("potentiometer: {}".format(data))

def loop():
    board.potentiometer.read(read_callback)
    board.sleep(0.1)

if __name__ == "__main__":
    while True:
        loop()
