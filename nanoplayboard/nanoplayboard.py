#!/usr/bin/python

import asyncio
from nanoplayboard.constants import NanoPlayBoardConstants
from nanoplayboard.pymata_core import PymataCore


class RGB:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    async def _set_color(self, r, g, b):
        d1 = r >> 1
        d2 = ((r & 0x01) << 6) | (g >> 2)
        d3 = ((g & 0x03) << 5) | (b >> 3)
        d4 = (b & 0x07) << 4
        data = [NanoPlayBoardConstants.RGB_SET_COLOR, d1, d2, d3, d4]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    async def _on(self):
        data = [NanoPlayBoardConstants.RGB_ON]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    async def _off(self):
        data = [NanoPlayBoardConstants.RGB_OFF]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    async def _toggle(self):
        data = [NanoPlayBoardConstants.RGB_TOGGLE]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    async def _set_intensity(self, intensity):
        data = [NanoPlayBoardConstants.RGB_SET_INTENSITY, intensity & 0x7F]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    def set_color(self, r, g, b):
        task = asyncio.ensure_future(self._set_color(r, g, b))
        self.loop.run_until_complete(task)

    def on(self):
        task = asyncio.ensure_future(self._on())
        self.loop.run_until_complete(task)

    def off(self):
        task = asyncio.ensure_future(self._off())
        self.loop.run_until_complete(task)

    def toggle(self):
        task = asyncio.ensure_future(self._toggle())
        self.loop.run_until_complete(task)

    def set_intensity(self, intensity):
        task = asyncio.ensure_future(self._set_intensity(intensity))
        self.loop.run_until_complete(task)


class Buzzer:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    async def _play_tone(self, frequency_hz, duration_ms):
        f1 = frequency_hz & 0x7F
        f2 = frequency_hz >> 7
        d1 = duration_ms & 0x7F
        d2 = duration_ms >> 7
        data = [NanoPlayBoardConstants.BUZZER_PLAY_TONE, f1, f2, d1, d2]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    async def _stop_tone(self):
        data = [NanoPlayBoardConstants.BUZZER_STOP_TONE]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    def play_tone(self, frequency_hz, duration_ms=0):
        task = asyncio.ensure_future(
            self._play_tone(frequency_hz, duration_ms))
        self.loop.run_until_complete(task)

    def stop_tone(self):
        task = asyncio.ensure_future(self._stop_tone())
        self.loop.run_until_complete(task)


class Potentiometer:

    def __init__(self, core, loop):
        self.core = core
        self.loop = loop

    async def _read(self):
        data = [NanoPlayBoardConstants.POTENTIOMETER_READ]
        await self.core._send_sysex(NanoPlayBoardConstants.COMMAND, data)

    def read(self, callback):
        task = asyncio.ensure_future(self._read())
        self.loop.run_until_complete(task)
        self.core._potentiometer_callback = callback


class NanoPlayBoard:

    def __init__(self):
        super().__init__()
        self.core = PymataCore()
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.core.start_aio())

        self.rgb = RGB(self.core, self.loop)
        self.buzzer = Buzzer(self.core, self.loop)
        self.potentiometer = Potentiometer(self.core, self.loop)

    def sleep(self, time):
        try:
            task = asyncio.ensure_future(self.core.sleep(time))
            self.loop.run_until_complete(task)

        except asyncio.CancelledError:
            pass
        except RuntimeError:
            pass
