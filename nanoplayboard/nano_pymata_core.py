""" 
NanoPyMataCore class.

This class is based on:
  - pymata_core.py developed by Alan Yorinks.
  - circuitplayground.py developed by Tony DiCola.

Copyright (c) 2015-16 Alan Yorinks All rights reserved.
Copyright (C) 2016 Tony DiCola.  All rights reserved.
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

import struct
import asyncio
from pymata_aio.pymata_core import PymataCore
from pymata_aio.private_constants import PrivateConstants
from nanoplayboard.nano_constants import NanoConstants


class NanoPymataCore(PymataCore):

    def __init__(self):
        super().__init__()

        # this dictionary for mapping incoming Firmata message types to
        # handlers for the messages
        self.command_dictionary = {PrivateConstants.REPORT_VERSION:
                                   self._report_version,
                                   PrivateConstants.REPORT_FIRMWARE:
                                       self._report_firmware,
                                   PrivateConstants.CAPABILITY_RESPONSE:
                                       self._capability_response,
                                   PrivateConstants.ANALOG_MAPPING_RESPONSE:
                                       self._analog_mapping_response,
                                   PrivateConstants.PIN_STATE_RESPONSE:
                                       self._pin_state_response,
                                   PrivateConstants.STRING_DATA:
                                       self._string_data,
                                   PrivateConstants.ANALOG_MESSAGE:
                                       self._analog_message,
                                   PrivateConstants.DIGITAL_MESSAGE:
                                       self._digital_message,
                                   PrivateConstants.I2C_REPLY:
                                       self._i2c_reply,
                                   PrivateConstants.SONAR_DATA:
                                       self._sonar_data,
                                   PrivateConstants.ENCODER_DATA:
                                       self._encoder_data,
                                   PrivateConstants.PIXY_DATA:
                                       self._pixy_data,
                                   NanoConstants.COMMAND:
                                       self._nanoplayboard_response}

        # report query results are stored in this dictionary
        self.query_reply_data = {PrivateConstants.REPORT_VERSION: '',
                                 PrivateConstants.STRING_DATA: '',
                                 PrivateConstants.REPORT_FIRMWARE: '',
                                 PrivateConstants.CAPABILITY_RESPONSE: None,
                                 PrivateConstants.ANALOG_MAPPING_RESPONSE: None,
                                 PrivateConstants.PIN_STATE_RESPONSE: None,
                                 NanoConstants.POTENTIOMETER_READ: None,
                                 NanoConstants.POTENTIOMETER_SCALE_TO: None,
                                 NanoConstants.LDR_READ: None,
                                 NanoConstants.LDR_SCALE_TO: None,
                                 NanoConstants.ROTARY_ENCODER_READ: None,
                                 NanoConstants.ULTRASOUND_READ: None}

        # callbacks
        self._potentiometer_callback = None
        self._ldr_callback = None
        self._rotary_encoder_callback = None
        self._ultrasound_callback = None

    '''
    Buzzer
    '''

    async def _buzzer_play_tone(self, frequency_hz, duration_ms):
        f1 = frequency_hz & 0x7F
        f2 = frequency_hz >> 7
        d1 = duration_ms & 0x7F
        d2 = duration_ms >> 7
        data = [NanoConstants.BUZZER_PLAY_TONE, f1, f2, d1, d2]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _buzzer_stop_tone(self):
        data = [NanoConstants.BUZZER_STOP_TONE]
        await self._send_sysex(NanoConstants.COMMAND, data)

    '''
    Rgb led
    '''

    async def _rgb_set_color(self, r, g, b):
        d1 = r >> 1
        d2 = ((r & 0x01) << 6) | (g >> 2)
        d3 = ((g & 0x03) << 5) | (b >> 3)
        d4 = (b & 0x07) << 4
        data = [NanoConstants.RGB_SET_COLOR, d1, d2, d3, d4]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _rgb_on(self):
        data = [NanoConstants.RGB_ON]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _rgb_off(self):
        data = [NanoConstants.RGB_OFF]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _rgb_toggle(self):
        data = [NanoConstants.RGB_TOGGLE]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _rgb_set_intensity(self, intensity):
        data = [NanoConstants.RGB_SET_INTENSITY, intensity & 0x7F]
        await self._send_sysex(NanoConstants.COMMAND, data)

    '''
    Potentiometer
    '''

    async def _potentiometer_read(self):
        if self.query_reply_data.get(NanoConstants.POTENTIOMETER_READ) == None:
            data = [NanoConstants.POTENTIOMETER_READ]
            await self._send_sysex(NanoConstants.COMMAND, data)
            while self.query_reply_data.get(NanoConstants.POTENTIOMETER_READ) == None:
                await asyncio.sleep(self.sleep_tune)
            value = self.query_reply_data.get(NanoConstants.POTENTIOMETER_READ)
            self.query_reply_data[NanoConstants.POTENTIOMETER_READ] = None
            return value

    async def _potentiometer_scale_to(self, to_low, to_high):
        if self.query_reply_data.get(NanoConstants.POTENTIOMETER_SCALE_TO) == None:
            l1 = to_low & 0x7F
            l2 = to_low >> 7
            h1 = to_high & 0x7F
            h2 = to_high >> 7
            data = [NanoConstants.POTENTIOMETER_SCALE_TO, l1, l2, h1, h2]
            await self._send_sysex(NanoConstants.COMMAND, data)
            while self.query_reply_data.get(NanoConstants.POTENTIOMETER_SCALE_TO) == None:
                await asyncio.sleep(self.sleep_tune)
            value = self.query_reply_data.get(
                NanoConstants.POTENTIOMETER_SCALE_TO)
            self.query_reply_data[NanoConstants.POTENTIOMETER_SCALE_TO] = None
            return value

    '''
    Ldr
    '''

    async def _ldr_read(self):
        if self.query_reply_data.get(NanoConstants.LDR_READ) == None:
            data = [NanoConstants.LDR_READ]
            await self._send_sysex(NanoConstants.COMMAND, data)
            while self.query_reply_data.get(NanoConstants.LDR_READ) == None:
                await asyncio.sleep(self.sleep_tune)
            value = self.query_reply_data.get(NanoConstants.LDR_READ)
            self.query_reply_data[NanoConstants.LDR_READ] = None
            return value

    async def _ldr_scale_to(self, to_low, to_high):
        if self.query_reply_data.get(NanoConstants.LDR_SCALE_TO) == None:
            l1 = to_low & 0x7F
            l2 = to_low >> 7
            h1 = to_high & 0x7F
            h2 = to_high >> 7
            data = [NanoConstants.LDR_SCALE_TO, l1, l2, h1, h2]
            await self._send_sysex(NanoConstants.COMMAND, data)
            while self.query_reply_data.get(NanoConstants.LDR_SCALE_TO) == None:
                await asyncio.sleep(self.sleep_tune)
            value = self.query_reply_data.get(
                NanoConstants.LDR_SCALE_TO)
            self.query_reply_data[NanoConstants.LDR_SCALE_TO] = None
            return value

    '''
    LedMatrix
    '''

    async def _ledmatrix_print_pattern(self, pattern):
        data = [NanoConstants.LEDMATRIX_PRINT_PATTERN]
        for p in pattern:
            data.append(p & 0x7F)
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _ledmatrix_print_number(self, number):
        data = [NanoConstants.LEDMATRIX_PRINT_NUMBER, number & 0x7F]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _ledmatrix_print_char(self, symbol):
        data = [NanoConstants.LEDMATRIX_PRINT_CHAR, ord(symbol) & 0x7F]
        await self._send_sysex(NanoConstants.COMMAND, data)

    async def _ledmatrix_print_message(self, message):
        data = [NanoConstants.LEDMATRIX_PRINT_STRING, len(message) & 0x7F]
        for symbol in message:
            data.append(ord(symbol) & 0x7F)
        await self._send_sysex(NanoConstants.COMMAND, data)

    '''
    Servo
    '''

    async def _servo_to(self, id, degrees):
        id = id & 0x7F
        d1 = degrees & 0x7F
        d2 = degrees >> 7
        data = [NanoConstants.SERVO_TO, id, d1, d2]
        await self._send_sysex(NanoConstants.COMMAND, data)

    '''
    RotaryEncoder
    '''

    async def _rotary_encoder_get_position(self):
        if self.query_reply_data.get(NanoConstants.ROTARY_ENCODER_READ) == None:
            data = [NanoConstants.ROTARY_ENCODER_READ]
            await self._send_sysex(NanoConstants.COMMAND, data)
            while self.query_reply_data.get(NanoConstants.ROTARY_ENCODER_READ) == None:
                await asyncio.sleep(self.sleep_tune)
            value = self.query_reply_data.get(NanoConstants.ROTARY_ENCODER_READ)
            self.query_reply_data[NanoConstants.ROTARY_ENCODER_READ] = None
            return value

    '''
    Ultrasound
    '''

    async def _ultrasound_read(self):
        if self.query_reply_data.get(NanoConstants.ULTRASOUND_READ) == None:
            data = [NanoConstants.ULTRASOUND_READ]
            await self._send_sysex(NanoConstants.COMMAND, data)
            while self.query_reply_data.get(NanoConstants.ULTRASOUND_READ) == None:
                await asyncio.sleep(self.sleep_tune)
            value = self.query_reply_data.get(NanoConstants.ULTRASOUND_READ)
            self.query_reply_data[NanoConstants.ULTRASOUND_READ] = None
            return value


    '''
    Firmata responses
    '''

    async def _nanoplayboard_response(self, data):
        if len(data) < 1:
            print("Received response with no data!")
            return

        command = data[1] & 0x7F

        if command == NanoConstants.POTENTIOMETER_READ:
            self._potentiometer_read_response(data)
        elif command == NanoConstants.POTENTIOMETER_SCALE_TO:
            self._potentiometer_scale_to_response(data)
        elif command == NanoConstants.LDR_READ:
            self._ldr_read_response(data)
        elif command == NanoConstants.LDR_SCALE_TO:
            self._ldr_scale_to_response(data)
        elif command == NanoConstants.ULTRASOUND_READ:
            self._ultrasound_read_response(data)

    def _potentiometer_read_response(self, data):
        pot_value = self._parse_firmata_uint16(data[3:-1])
        self.query_reply_data[NanoConstants.POTENTIOMETER_READ] = pot_value
        if self._potentiometer_callback is not None:
            self._potentiometer_callback(pot_value)

    def _potentiometer_scale_to_response(self, data):
        pot_value = self._parse_firmata_uint16(data[3:-1])
        self.query_reply_data[NanoConstants.POTENTIOMETER_SCALE_TO] = pot_value
        if self._potentiometer_callback is not None:
            self._potentiometer_callback(pot_value)

    def _ldr_read_response(self, data):
        ldr_value = self._parse_firmata_uint16(data[3:-1])
        self.query_reply_data[NanoConstants.LDR_READ] = ldr_value
        if self._ldr_callback is not None:
            self._ldr_callback(ldr_value)

    def _ldr_scale_to_response(self, data):
        ldr_value = self._parse_firmata_uint16(data[3:-1])
        self.query_reply_data[NanoConstants.LDR_SCALE_TO] = ldr_value
        if self._ldr_callback is not None:
            self._ldr_callback(ldr_value)

    def _ultrasound_read_response(self, data):
        ultrasound_value = self._parse_firmata_uint16(data[3:-1])
        self.query_reply_data[NanoConstants.ULTRASOUND_READ] = ultrasound_value
        if self._ultrasound_callback is not None:
            self._ultrasound_callback(ultrasound_value)

    '''
    Utilities
    '''

    def _parse_firmata_byte(self, data):
        """Parse a byte value from two 7-bit byte firmata response bytes."""
        if len(data) != 2:
            raise ValueError(
                'Expected 2 bytes of firmata repsonse for a byte value!')
        return (data[0] & 0x7F) | ((data[1] & 0x01) << 7)

    def _parse_firmata_uint16(self, data):
        """Parse a 2 byte unsigned integer value from a 7-bit byte firmata response
        byte array.  Each pair of firmata 7-bit response bytes represents a single
        byte of int data so there should be 4 firmata response bytes total.
        """
        if len(data) != 4:
            raise ValueError(
                'Expected 4 bytes of firmata response for int value!')
        # Convert 2 7-bit bytes in little endian format to 1 8-bit byte for each
        # of the two unsigned int bytes.
        raw_bytes = bytearray(2)
        for i in range(2):
            raw_bytes[i] = self._parse_firmata_byte(data[i * 2:i * 2 + 2])
        # Use struct unpack to convert to unsigned short value.
        return struct.unpack('<H', raw_bytes)[0]

    def _parse_firmata_long(self, data):
        """Parse a 4 byte signed long integer value from a 7-bit byte firmata response
        byte array.  Each pair of firmata 7-bit response bytes represents a single
        byte of long data so there should be 8 firmata response bytes total.
        """
        if len(data) != 8:
            raise ValueError(
                'Expected 8 bytes of firmata response for long value!')
        # Convert 2 7-bit bytes in little endian format to 1 8-bit byte for each
        # of the four long bytes.
        raw_bytes = bytearray(4)
        for i in range(4):
            raw_bytes[i] = self._parse_firmata_byte(data[i * 2:i * 2 + 2])
        # Use struct unpack to convert to long value.
        return struct.unpack('<l', raw_bytes)[0]
