""" 
NanoPlayBoard class.

This class is based on:
  - pymata_core.py developed by Alan Yorinks.

Copyright (c) 2015-16 Alan Yorinks All rights reserved.
Copyright (C) 2016 Jose Juan Sanchez.  All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
"""

import asyncio
from nanoplayboard.nano_pymata_core import NanoPymataCore
from functools import singledispatch


class RGB:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def set_color(self, r, g, b):
        task = asyncio.ensure_future(self.core._rgb_set_color(r, g, b))
        self.loop.run_until_complete(task)

    def on(self):
        task = asyncio.ensure_future(self.core._rgb_on())
        self.loop.run_until_complete(task)

    def off(self):
        task = asyncio.ensure_future(self.core._rgb_off())
        self.loop.run_until_complete(task)

    def toggle(self):
        task = asyncio.ensure_future(self.core._rgb_toggle())
        self.loop.run_until_complete(task)

    def set_intensity(self, intensity):
        task = asyncio.ensure_future(self.core._rgb_set_intensity(intensity))
        self.loop.run_until_complete(task)


class Buzzer:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def play_tone(self, frequency_hz, duration_ms=0):
        task = asyncio.ensure_future(
            self.core._buzzer_play_tone(frequency_hz, duration_ms))
        self.loop.run_until_complete(task)

    def stop_tone(self):
        task = asyncio.ensure_future(self.core._buzzer_stop_tone())
        self.loop.run_until_complete(task)


class Potentiometer:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def read(self, callback=None):
        task = asyncio.ensure_future(self.core._potentiometer_read())
        value = self.loop.run_until_complete(task)
        self.core._potentiometer_callback = callback
        return value

    def scale_to(self, to_low, to_high, callback=None):
        task = asyncio.ensure_future(
            self.core._potentiometer_scale_to(to_low, to_high))
        value = self.loop.run_until_complete(task)
        self.core._potentiometer_callback = callback
        return value


class Ldr:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def read(self, callback=None):
        task = asyncio.ensure_future(self.core._ldr_read())
        value = self.loop.run_until_complete(task)
        self.core._ldr_callback = callback
        return value

    def scale_to(self, to_low, to_high, callback=None):
        task = asyncio.ensure_future(
            self.core._ldr_scale_to(to_low, to_high))
        value = self.loop.run_until_complete(task)
        self.core._ldr_callback = callback
        return value


class LedMatrix:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def print_pattern(self, pattern):
        task = asyncio.ensure_future(
            self.core._ledmatrix_print_pattern(pattern))
        self.loop.run_until_complete(task)

    def print_number(self, number):
        task = asyncio.ensure_future(
            self.core._ledmatrix_print_number(number))
        self.loop.run_until_complete(task)

    def print_char(self, symbol):
        task = asyncio.ensure_future(
            self.core._ledmatrix_print_char(symbol))
        self.loop.run_until_complete(task)

    def print_message(self, message):
        task = asyncio.ensure_future(
            self.core._ledmatrix_print_message(message))
        self.loop.run_until_complete(task)


class NanoServo:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def to(self, id, degrees):
        task = asyncio.ensure_future(
            self.core._servo_to(id, degrees))
        self.loop.run_until_complete(task)


class RotaryEncoder:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def read(self, callback=None):
        task = asyncio.ensure_future(self.core._rotary_encoder_get_position())
        value = self.loop.run_until_complete(task)
        self.core._rotary_encoder_callback = callback
        return value

class Ultrasound:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    def read(self, callback=None):
        task = asyncio.ensure_future(self.core._ultrasound_read())
        value = self.loop.run_until_complete(task)
        self.core._ultrasound_callback = callback
        return value

class NanoPlayBoard:

    def __init__(self):
        super().__init__()
        self.core = NanoPymataCore()
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.core.start_aio())

        self.rgb = RGB(self.core, self.loop)
        self.buzzer = Buzzer(self.core, self.loop)
        self.potentiometer = Potentiometer(self.core, self.loop)
        self.ldr = Ldr(self.core, self.loop)
        self.ledmatrix = LedMatrix(self.core, self.loop)
        self.servo = [NanoServo(self.core, self.loop)] * 2
        self.ultrasound = Ultrasound(self.core, self.loop)
        self.rotaryencoder = RotaryEncoder(self.core, self.loop)

    def sleep(self, time):
        try:
            task = asyncio.ensure_future(self.core.sleep(time))
            self.loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass
        except RuntimeError:
            pass
