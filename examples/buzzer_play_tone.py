#!/usr/bin/python

from nanoplayboard.nanoplayboard import NanoPlayBoard

board = NanoPlayBoard()


def loop():
    board.buzzer.play_tone(440)
    board.sleep(0.15)
    board.buzzer.stop_tone()
    board.sleep(1)


if __name__ == "__main__":
    while True:
        loop()
