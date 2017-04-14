#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()
message = "Hello world!"

def setup():
    board.ledmatrix.print_message(message)

def loop():
    pass

if __name__ == "__main__":
    setup()
    while True:
        loop()
