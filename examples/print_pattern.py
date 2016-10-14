#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()
pattern = [16, 72, 8, 72, 16]

def loop():
    board.ledmatrix.print_pattern(pattern)
    board.sleep(0.020)

if __name__ == "__main__":
    while True:
        loop()
