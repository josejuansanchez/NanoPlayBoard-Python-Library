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
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, [Constants.NPB_RGB_ON])

    async def _off(self):
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, [Constants.NPB_RGB_OFF])

    async def _toggle(self):
        await self.pymata3.core._send_sysex(Constants.NPB_COMMAND, [Constants.NPB_RGB_TOGGLE])

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


class NanoPlayBoard(PyMata3):

    def __init__(self):
        super().__init__()
        self.rgb = RGB(self)
