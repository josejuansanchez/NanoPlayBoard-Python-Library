#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()


def loop():
    board.rgb.toggle()
    board.sleep(1)

if __name__ == "__main__":
    while True:
        loop()
