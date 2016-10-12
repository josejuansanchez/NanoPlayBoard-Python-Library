#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()


def setup():
    board.rgb.on()


def loop():
    for intensity in range(0, 101, 25):
        board.rgb.set_intensity(intensity)
        print(intensity)
        board.sleep(0.5)

    for intensity in range(100, 0, -25):
        board.rgb.set_intensity(intensity)
        print(intensity)
        board.sleep(0.5)


if __name__ == "__main__":
    setup()
    while True:
        loop()
