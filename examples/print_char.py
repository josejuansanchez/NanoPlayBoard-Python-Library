#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()
message = "Hola mundo "

def loop():
    for symbol in message:
        board.ledmatrix.print_char(symbol)
        board.sleep(0.20)

if __name__ == "__main__":
    while True:
        loop()
