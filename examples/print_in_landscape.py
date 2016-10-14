#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()

def loop():
    for number in range(0, 100):
        board.ledmatrix.print_in_landscape(number)
        board.sleep(0.020)

if __name__ == "__main__":
    while True:
        loop()
