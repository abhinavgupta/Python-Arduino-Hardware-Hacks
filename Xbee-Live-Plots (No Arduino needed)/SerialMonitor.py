#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Queue
import threading
from xbee import XBee
import serial
import dict_lut

ADC_RESOLUTION = 1024.00
RESISTANCE = 7.990
BAUD_RATE = 9600
PORT = '/dev/ttyACM0'

class SerialMonitorThread(threading.Thread):
    """ A thread for monitoring a serial port. The serial port is
        opened when the thread is started.

        data_q:
            Queue for received data. Items in the queue are
            (data, timestamp) pairs, where data is a binary
            string representing the received data, and timestamp
            is the time elapsed from the thread's start (in
            seconds).

        error_q:
            Queue for error messages. In particular, if the
            serial port fails to open for some reason, an error
            is placed into this queue.
    """
    def __init__(self, data_q, error_q):
        threading.Thread.__init__(self)

        self.serial_port = None
        self.data_q = data_q
        self.error_q = error_q

        self.alive = threading.Event()
        self.alive.set()

    def run(self):
        try:
            if self.serial_port:
                self.serial_port.close()
            # Port hardcoded :)
            self.serial_port = serial.Serial(PORT, BAUD_RATE)
        except serial.SerialException, e:
            self.error_q.put(e.message)
            return

        # Restart the clock
        time.clock()

        while self.alive.isSet():
            # Reading 1 byte, followed by whatever is left in the
            # read buffer, as suggested by the developer of
            # PySerial.
            # 

			# XBee library used from this point:
			xbee = XBee(self.serial_port)
			#Read Response frame now:
			response = xbee.wait_read_frame()
			#Read the sample part from the respnase frame taking the first value (In case you use multiple sensors):
			sample = response['samples'][0]
			#ADC-0 is the one in my setup
			adc_value = sample['adc-0']
			#Changing ADC value to Resistance and subsequent mapping of Resistance to Temperature in the next three steps 
			# FIXME: Change for your specific use, this works fine for my use just used the highlighter to point this fact
			temp_value = ADC_RESOLUTION/adc_value - 1
			thermistor_value = (RESISTANCE/temp_value) + 0.24
			temperature_value = dict_lut.closest_match(thermistor_value)
			#Add Time stamp here:
			timestamp = time.clock()
			self.data_q.put((temperature_value, timestamp))

        # clean up
        if self.serial_port:
            self.serial_port.close()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

