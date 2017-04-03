"""
Implements the MPU6050 sensor for the framework. Only the I2C adress can be configured, either 0x68 or 0x69. There are more options possible, since the ADC on the chip has more settings, but by now we only use the defaults, which are working good enough for us.
"""
import smbus2
import math
import logging

from raspyre.sensor import Sensor
from raspyre.record import Record

import time


class MPU6050 (Sensor) :
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    sensor_attributes = {'accx': ("m/s^2", "d"),
                         'accy': ("m/s^2", "d"),
                         'accz': ("m/s^2", "d"),
                         'temperature': ("C", "d"),
                         'gyrox': ("g", "d"),
                         'gyroy': ("g", "d"),
                         'gyroz': ("g", "d")}

    #dictionary of the register adresses and scale factors for the measureable pins
    #these values are taken from the data sheet

    def __init__ (self, address = 0x68 ):
        self.address = address
        self.bus = smbus2.SMBus(1)
        #wake up the mpu, it starts in sleep mode
        self.bus.write_byte_data(address , self.power_mgmt_1 , 0)
        #set sps to max
        self.bus.write_byte_data(address , 0x19 , 0)
        self.bus.write_byte_data(address , 0x1a , 0)

        logger = logging.getLogger(__name__)
        logger.info('MPU6050 instantiated on address {adr}.'.format(adr=hex(address)))

    def getFastRecord(self):
        register_values = self.bus.read_i2c_block_data(self.address,0x3b,15)
        accx = self.convert2C((register_values[0] << 8) + register_values[1] ) / 16384.0
        accy = self.convert2C((register_values[2] << 8) + register_values[3] ) / 16384.0
        accz = self.convert2C((register_values[4] << 8) + register_values[5] ) / 16384.0
        return (time.time(), accx, accy, accz)

    def getRecord(self, *args) :
        """
        The sensor always samples all possible values. Only the requested are returned.
        """
        record = Record()
        register_values = self.bus.read_i2c_block_data(self.address,0x3b,14)
        values = {}
        values['accx'] = self._convert2C((register_values[0] << 8) + register_values[1] ) / 16384.0
        values['accy'] = self._convert2C((register_values[2] << 8) + register_values[3] ) / 16384.0
        values['accz'] = self._convert2C((register_values[4] << 8) + register_values[5] ) / 16384.0
        values['temperature'] = self._convert2C((register_values[6] << 8) + register_values[7] ) / 340.0 + 36.53
        values['gyrox'] = self._convert2C((register_values[8] << 8) + register_values[9] ) / 131.0
        values['gyroy'] = self._convert2C((register_values[10] << 8) + register_values[11] ) / 131.0
        values['gyroz'] = self._convert2C((register_values[12] << 8) + register_values[13] ) / 131.0
        for request in args :
            try:
                record[request] = values[request]
            except:
                raise AttributeError('Invalid value requested: {req}.'.format(req=request))
        return record
    def getAttributes(self) :
        return self.sensor_attributes.keys()

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def _convert2C(self, val):
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def build(**kwargs) :
    addrstr = kwargs.get('address' , '0x68')
    addr = int(addrstr ,16)
    sensor = MPU6050(addr)
    logger = logging.getLogger(__name__)
    logger.info("MPU6050 initialised on address {}".format(addrstr))
    return sensor


