#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()


def loop():
    board.rgb.on()
    board.sleep(1)
    board.rgb.off()
    board.sleep(1)

if __name__ == "__main__":
    while True:
        loop()
