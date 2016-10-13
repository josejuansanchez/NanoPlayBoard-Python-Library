#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def loop():
    value = board.ldr.scale_to(0, 100)
    print("Ldr: {}".format(value))
    board.sleep(0.1)

if __name__ == "__main__":
    while True:
        loop()
