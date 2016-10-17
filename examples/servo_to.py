#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()


def loop():
    for i in range(0,181):
        print(i)
        board.servo[0].to(0, i)
        board.sleep(0.05)

    for i in range(0,181):
        print(i)
        board.servo[0].to(1, i)
        board.sleep(0.05)

if __name__ == "__main__":
    while True:
        loop()
