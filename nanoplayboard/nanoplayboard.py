import asyncio
from nanoplayboard.nano_pymata_core import NanoPymataCore


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


class NanoPlayBoard:

    def __init__(self):
        super().__init__()
        self.core = NanoPymataCore()
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
