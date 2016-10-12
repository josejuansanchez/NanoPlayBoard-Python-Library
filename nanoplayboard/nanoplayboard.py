#!/usr/bin/python

import asyncio
from pymata_aio.pymata3 import PyMata3
from nanoplayboard.constants import Constants


class RGB:

    def __init__(self, pymata3):
        self.pymata3 = pymata3

    async def _set_color(self, r, g, b):
        d1 = r >> 1
        d2 = ((r & 0x01) << 6) | (g >> 2)
        d3 = ((g & 0x03) << 5) | (b >> 3)
        d4 = (b & 0x07) << 4
        data = [Constants.NPB_RGB_SET_COLOR, d1, d2, d3, d4]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    async def _on(self):
        data = [Constants.NPB_RGB_ON]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    async def _off(self):
        data = [Constants.NPB_RGB_OFF]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    async def _toggle(self):
        data = [Constants.NPB_RGB_TOGGLE]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    async def _set_intensity(self, intensity):
        data = [Constants.NPB_RGB_SET_INTENSITY, intensity & 0x7F]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    def set_color(self, r, g, b):
        task = asyncio.ensure_future(self._set_color(r, g, b))
        self.pymata3.loop.run_until_complete(task)

    def on(self):
        task = asyncio.ensure_future(self._on())
        self.pymata3.loop.run_until_complete(task)

    def off(self):
        task = asyncio.ensure_future(self._off())
        self.pymata3.loop.run_until_complete(task)

    def toggle(self):
        task = asyncio.ensure_future(self._toggle())
        self.pymata3.loop.run_until_complete(task)

    def set_intensity(self, intensity):
        task = asyncio.ensure_future(self._set_intensity(intensity))
        self.pymata3.loop.run_until_complete(task)


class Buzzer:

    def __init__(self, pymata3):
        self.pymata3 = pymata3

    async def _play_tone(self, frequency_hz, duration_ms):
        f1 = frequency_hz & 0x7F
        f2 = frequency_hz >> 7
        d1 = duration_ms & 0x7F
        d2 = duration_ms >> 7
        data = [Constants.NPG_BUZZER_PLAY_TONE, f1, f2, d1, d2]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    async def _stop_tone(self):
        data = [Constants.NPG_BUZZER_STOP_TONE]
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, data)

    def play_tone(self, frequency_hz, duration_ms=0):
        task = asyncio.ensure_future(
            self._play_tone(frequency_hz, duration_ms))
        self.pymata3.loop.run_until_complete(task)

    def stop_tone(self):
        task = asyncio.ensure_future(self._stop_tone())
        self.pymata3.loop.run_until_complete(task)


class NanoPlayBoard(PyMata3):

    def __init__(self):
        super().__init__()
        self.rgb = RGB(self)
        self.buzzer = Buzzer(self)
