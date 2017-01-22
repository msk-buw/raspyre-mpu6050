from raspyre.sensors.mpu6050 import MPU6050
from raspyre import sensorbuilder as sb
import smbus2
from mock import MagicMock
import pytest

# NEW STYLE FIXTURE!!!
@pytest.fixture
def mpu6050_bus(mocker):
    mock_smbus = mocker.patch.object(smbus2, 'SMBus', autospec=True)
    mpu = MPU6050(0x68)
    return mpu

def test__MPU6050_init2(mpu6050_bus, mocker):
    bus = mpu6050_bus.bus
    #bus.read_byte_data = mocker.Mock()
    bus.read_byte_data.side_effect = [1, 1]
    i = mpu6050_bus.read_word(23)
    assert i == 0x0101
    bus.read_byte_data.assert_any_call(0x68, 23)
    bus.read_byte_data.assert_any_call(0x68, 24)


def test__MPU6050_init(mocker):
    mock_smbus = mocker.patch.object(smbus2, 'SMBus', autospec=True)
    #bus = mocker.Mock()
    #mock_smbus.return_value = bus
    mpu = MPU6050(0x68)
    #print bus.write_byte_data.call_args_list

