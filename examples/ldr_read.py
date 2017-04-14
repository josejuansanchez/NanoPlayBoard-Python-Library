#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def loop():
    value = board.ldr.read()
    print("Ldr: {}".format(value))
    board.sleep(0.1)

if __name__ == "__main__":
    while True:
        loop()
