#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def read_callback(data):
    print("Ultrasound: {}".format(data))

def loop():
    board.ultrasound.read(read_callback)
    board.sleep(0.1)

if __name__ == "__main__":
    while True:
        loop()
