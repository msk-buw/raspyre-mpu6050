from raspyre.sensors.mpu6050 import MPU6050
from raspyre import sensorbuilder as sb
import smbus
from mock import MagicMock
import pytest

@pytest.fixture
def smbus_mock(mocker):
    return MagicMock(smbus.SMBus)
    #return mocker.patch.object(smbus, 'smbus.SMBus', autospech=True)

@pytest.fixture
def mpu6050_test_sensor(monkeypatch, smbus_mock):
    monkeypatch.setattr('smbus.SMBus', smbus_mock)
    test_sensor = MPU6050(0x68)
    return test_sensor

def test_createSensor(mpu6050_test_sensor):
    assert mpu6050_test_sensor.address == 0x68

def test_sensorbuilder_MPU6050(mpu6050_test_sensor):
    sb_built_sensor = sb.createSensor(type="mpu6050", address="0x68")
    #assert mpu6050_test_sensor.address == sb_built_sensor.address
