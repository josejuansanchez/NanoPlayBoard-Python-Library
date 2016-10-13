#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def ldr_callback(data):
    print("ldr: {}".format(data))

def loop():
    board.ldr.read(ldr_callback)
    board.sleep(0.1)

if __name__ == "__main__":
    while True:
        loop()
