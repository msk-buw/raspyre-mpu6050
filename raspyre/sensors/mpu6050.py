"""
Implements the MPU6050 sensor for the framework. Only the I2C adress can be configured, either 0x68 or 0x69. There are more options possible, since the ADC on the chip has more settings, but by now we only use the defaults, which are working good enough for us.
"""
import smbus2
import logging

from raspyre.sensor import Sensor
from raspyre.record import Record

import time

class MPU6050 (Sensor) :
    sensor_attributes = {'accx': ("g", "d"),
                         'accy': ("g", "d"),
                         'accz': ("g", "d"),
                         'temperature': ("C", "d"),
                         'gyrox': ("deg/s", "d"),
                         'gyroy': ("deg/s", "d"),
                         'gyroz': ("deg/s", "d")}

    POWER_MGMT_1 = 0x6b
    POWER_MGMT_2 = 0x6c

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    def __init__ (self, address=0x68, accel_range=0x00):
        self.address = address
        self.bus = smbus2.SMBus(1)
        #wake up the mpu, it starts in sleep mode
        self.bus.write_byte_data(self.address , self.POWER_MGMT_1 , 0)
        #set sps to max
        self.bus.write_byte_data(self.address , 0x19 , 0)
        self.bus.write_byte_data(self.address , 0x1a , 0)

        # set accelerometer range
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)
        self.accel_scale = ACCEL_SCALE_MODIFIER_2G

        if accel_range != 0x00:
            if accel_range not in [self.ACCEL_RANGE_2G, self.ACCEL_RANGE_4G, self.ACCEL_RANGE_8G, self.ACCEL_RANGE_16G]:
                raise ValueError("ACCEL_RANGE invalid! Please specify range in [0x00, 0x08, 0x10, 0x18]")
            self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)
            if accel_range == self.ACCEL_RANGE_4G:
                self.accel_scale = self.ACCEL_SCALE_MODIFIER_4G
            elif accel_range == self.ACCEL_RANGE_8G:
                self.accel_scale = self.ACCEL_SCALE_MODIFIER_8G
            elif accel_range == self.ACCEL_RANGE_16G:
                self.accel_scale = self.ACCEL_SCALE_MODIFIER_16G

        logger = logging.getLogger(__name__)
        logger.info('MPU6050 instantiated on address {adr}.'.format(adr=hex(address)))

    def getFastRecord(self):
        register_values = self.bus.read_i2c_block_data(self.address,0x3b,15)
        accx = self.convert2C((register_values[0] << 8) + register_values[1] ) / self.accel_scale
        accy = self.convert2C((register_values[2] << 8) + register_values[3] ) / self.accel_scale
        accz = self.convert2C((register_values[4] << 8) + register_values[5] ) / self.accel_scale
        return (time.time(), accx, accy, accz)

    def getRecord(self, *args) :
        """
        The sensor always samples all possible values. Only the requested are returned.
        """
        record = Record()
        values = {}
        # perform only 6 byte read when only accelerometer data is requested
        if not any(channel in ['temperature', 'gyrox', 'gyroy', 'gyroz'] for channel in args):
            register_values = self.bus.read_i2c_block_data(self.address,0x3b,6)
        else:  # fetch complete register block
            register_values = self.bus.read_i2c_block_data(self.address,0x3b,14)
            values['temperature'] = self._convert2C((register_values[6] << 8) + register_values[7] ) / 340.0 + 36.53
            values['gyrox'] = self._convert2C((register_values[8] << 8) + register_values[9] ) / self.GYRO_SCALE_MODIFIER_250DEG
            values['gyroy'] = self._convert2C((register_values[10] << 8) + register_values[11] ) / self.GYRO_SCALE_MODIFIER_250DEG
            values['gyroz'] = self._convert2C((register_values[12] << 8) + register_values[13] ) / self.GYRO_SCALE_MODIFIER_250DEG
        values['accx'] = self._convert2C((register_values[0] << 8) + register_values[1] ) / self.accel_scale
        values['accy'] = self._convert2C((register_values[2] << 8) + register_values[3] ) / self.accel_scale
        values['accz'] = self._convert2C((register_values[4] << 8) + register_values[5] ) / self.accel_scale
        for request in args:
            record[request] = values[request]
        return record

    def getAttributes(self):
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

