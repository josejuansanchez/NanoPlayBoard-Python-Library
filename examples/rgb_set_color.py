#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()


def loop():
    board.rgb.set_color(255, 0, 0)
    board.sleep(1)
    board.rgb.set_color(0, 255, 0)
    board.sleep(1)
    board.rgb.set_color(0, 0, 255)
    board.sleep(1)

if __name__ == "__main__":
    while True:
        loop()
