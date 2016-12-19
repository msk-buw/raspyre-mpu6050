from raspyre.sensors.mpu6050 import MPU6050
from raspyre import sensorbuilder as sb
import smbus
from mock import MagicMock
import pytest

@pytest.fixture
def smbus_mock():
    return MagicMock(spidev.SpiDev)

@pytest.fixture
def fs_test_sensor(monkeypatch, spidev_mock):
    monkeypatch.setattr('spidev.SpiDev', spidev_mock)
    test_sensor = FirstSensor(0)
    return test_sensor

def test_createSensor(fs_test_sensor):
    assert fs_test_sensor.axes == ['acc0', 'acc1']
    assert fs_test_sensor.cshigh == False
    assert fs_test_sensor.spi.bits_per_word == 8
    assert fs_test_sensor.spi.max_speed_hz == 5000000
    fs_test_sensor.spi.open.assert_called_once_with(0, 0)

def test_sensorbuilder_FirstSensor(fs_test_sensor):
    sb_built_sensor = sb.createSensor(type="firstsensor", channel=0)
    assert fs_test_sensor.axes == sb_built_sensor.axes
    assert fs_test_sensor.cshigh == sb_built_sensor.cshigh

def test_del(monkeypatch):
    spidev_mock = MagicMock(spidev.SpiDev)
    monkeypatch.setattr('spidev.SpiDev', spidev_mock)
    test_sensor = FirstSensor(0)
    del test_sensor
    assert spidev_mock.close.called_once_with()

def test__readSys(fs_test_sensor):
    fs_test_sensor._readSys(0)
    fs_test_sensor.spi.xfer2.assert_called_with([0x7C, 0, 0x01])
    fs_test_sensor._readSys(51)
    fs_test_sensor.spi.xfer2.assert_called_with([0x7C, 51, 0x01])
    with pytest.raises(AttributeError):
        fs_test_sensor._readSys(-1)
    with pytest.raises(AttributeError):
        fs_test_sensor._readSys(52)

#    def test__byteArrayToInt(self):
#        data1 = 0
#        data2 = 0
#        with patch('framework.sensors.firstsensor.firstsensor.sys') as sys_mock:
#            type(sys_mock).byteorder = 'little'
#            data1 = self.mock_sensor._byteArrayToInt([0xFF, 0xEE, 0xDD, 0xCC])
#            type(sys_mock).byteorder = 'big'
#            data2 = self.mock_sensor._byteArrayToInt([0xCC, 0xDD, 0xEE, 0xFF])
#            self.assertEqual(data1, data2)
#
#            with self.assertRaises(AttributeError):
#                type(sys_mock).byteorder = 'mixed'
#                self.mock_sensor._byteArrayToInt([0, 1, 2, 3])
#            with self.assertRaises(AttributeError):
#                self.mock_sensor._byteArrayToInt([0, 1, 2])
#            with self.assertRaises(AttributeError):
#                self.mock_sensor._byteArrayToInt(42)
#
#    def test__intToBigEndianByteArray(self):
#        result = self.mock_sensor._intToBigEndianByteArray(0xAABBCCDD)
#        self.assertEqual(result, [0xAA, 0xBB, 0xCC, 0xDD])
#
#    def test__readRegister(self):
#        self.spidev_mock.xfer2.return_value = [0x58, 1, 2, 3, 4]
#        data = self.mock_sensor._readRegister()
#        self.spidev_mock.xfer2.assert_called_with([0x58, 0, 0, 0, 0])
#        self.assertEqual(data, 0x01020304)
#
#    def test_readRegister(self):
#        self.spidev_mock.xfer2.return_value = [0x58, 0xAA, 0xBB, 0xCC, 0xDD]
#        with patch.object(self.mock_sensor, "_readSys") as mock__readSys:
#            mock__readSys.return_value = None
#            data = self.mock_sensor.readRegister(42)
#            self.assertEqual(data, 0xAABBCCDD)
#
#    def test__changeBits(self):
#        result = self.mock_sensor._changeBits(0, 0xFFFFFFFF, 0, 31)
#        self.assertEqual(result, 0b11111111111111111111111111111111)
#        for i in range(0, 32 - 3):
#            result = self.mock_sensor._changeBits(0, 0b1010, i, i + 3)
#            self.assertEqual(result, 0b1010 << i)
#            result = self.mock_sensor._changeBits(0, 0b0101, i, i + 3)
#            self.assertEqual(result, 0b0101 << i)
#            result = self.mock_sensor._changeBits(0xFFFFFFFF, 0b0000, i, i + 3)
#            self.assertEqual(result, 0xFFFFFFFF - (0b1111 << i))
#        with self.assertRaises(AttributeError):
#            result = self.mock_sensor._changeBits(0, 256, 0, 7)
#        with self.assertRaises(AttributeError):
#            result = self.mock_sensor._changeBits(0, -1, 0, 31)
#        with self.assertRaises(AttributeError):
#            result = self.mock_sensor.changeBits(0, 0xFF, -1, 31)
#        with self.assertRaises(AttributeError):
#            result = self.mock_sensor.changeBits(0, 0xFF, 0, 32)
#
#    def test__setParameter(self):
#        with patch.object(self.mock_sensor, "_readSys") as mock__readSys:
#            mock__readSys.return_value = None
#            with patch.object(self.mock_sensor, "_readRegister") as mock__readRegister:
#                mock__readRegister.return_value = 0x00000000
#                self.mock_sensor._setParameter(0, 0, 31, 0xFFFFFFFF)
#                mock__readSys.assert_called_once_with(0)
#                call_list = [0x78, 0xFF, 0xFF, 0xFF, 0xFF, 0, 0x02]
#                self.spidev_mock.xfer2.assert_called_once_with(call_list)
#
#                mock__readSys.reset_mock()
#                self.spidev_mock.reset_mock()
#                mock__readRegister.return_value = 0xCCCCCCCC
#                self.mock_sensor._setParameter(42, 8, 24, 0x12AB)
#                mock__readSys.assert_called_once_with(42)
#                call_list = [0x78, 0xCC, 0x12, 0xAB, 0xCC, 42, 0x02]
#                self.spidev_mock.xfer2.assert_called_once_with(call_list)
#
#                mock__readSys.reset_mock()
#                self.spidev_mock.reset_mock()
#                self.mock_sensor._setParameter(51, 0, 31, 0x12AB34EF)
#                mock__readSys.assert_called_once_with(51)
#                call_list = [0x78, 0x12, 0xAB, 0x34, 0xEF, 51, 0x02]
#                self.spidev_mock.xfer2.assert_called_once_with(call_list)
#
#                with self.assertRaises(AttributeError):
#                    self.mock_sensor._setParameter(-1, 0, 31, 0xFFFFFFFF)
#                with self.assertRaises(AttributeError):
#                    self.mock_sensor._setParameter(52, 0, 31, 0xFFFFFFFF)
#                with self.assertRaises(AttributeError):
#                    self.mock_sensor._setParameter(0, 0, 7, 0x100)
#
#    def test_setParameter(self):
#        with patch.object(self.mock_sensor, "_setParameter") as mock__setParameter:
#            mock__setParameter.return_value = None
#            # test all possible Parameters with maximum and maximum + 1
#            REGISTER_MAP = self.mock_sensor.REGISTER_MAP
#            self.assertEqual(len(REGISTER_MAP), 28)
#            for parameter_name, parameters in REGISTER_MAP.items():
#                (address, start_bit, end_bit) = parameters
#                max_value = 2**(end_bit + 1 - start_bit)-1
#                mock__setParameter.reset_mock()
#                self.mock_sensor.setParameter(parameter_name, max_value)
#                mock__setParameter.assert_called_once_with(address, start_bit,
#                                                           end_bit, max_value)
#
#            with self.assertRaises(AttributeError):
#                self.mock_sensor.setParameter('PARAMETER_THAT_DOES_NOT_EXIST', 42)
#
#    def test__readCompleteRegister(self):
#        with patch.object(self.mock_sensor, "readRegister") as mock_readRegister:
#            register_mock_data = [0x01020304, 0x05060708, 0x090a0b0c, 0x0d0e0f10,
#                                  0x11121314, 0x15161718, 0x191a1b1c, 0x1d1e1f20,
#                                  0x21222324, 0x25262728, 0x292a2b2c, 0x2d2e2f30,
#                                  0x31323334, 0x35363738, 0x393a3b3c, 0x3d3e3f40,
#                                  0x41424344, 0x45464748, 0x494a4b4c, 0x4d4e4f50,
#                                  0x51525354, 0x55565758, 0x595a5b5c, 0x5d5e5f60,
#                                  0x61626364, 0x65666768, 0x696a6b6c, 0x6d6e6f70,
#                                  0x71727374, 0x75767778, 0x797a7b7c, 0x7d7e7f80,
#                                  0x81828384, 0x85868788, 0x898a8b8c, 0x8d8e8f90,
#                                  0x91929394, 0x95969798, 0x999a9b9c, 0x9d9e9fa0,
#                                  0xa1a2a3a4, 0xa5a6a7a8, 0xa9aaabac, 0xadaeafb0,
#                                  0xb1b2b3b4, 0xb5b6b7b8, 0xb9babbbc, 0xbdbebfc0,
#                                  0xc1c2c3c4, 0xc5c6c7c8, 0xc9cacbcc, 0xcdcecfd0]
#            mock_readRegister.side_effect = register_mock_data
#            register_data = self.mock_sensor._readCompleteRegister()
#            self.assertEqual(len(register_mock_data), 52)
#            self.assertEqual(register_mock_data, register_data)
#
#if __name__ == '__main__':
#    main()
