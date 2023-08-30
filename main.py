from db import DataBase
import time
from pymodbus.client import ModbusSerialClient as ModbusClient


client = ModbusClient(
    method='rtu', port='COM2', timeout=2, stopbits=1, bytesize=8, parity='N', baudrate=19200
)
success = client.connect()


def read_ans_save_one_device(sensor):
    unit = sensor['unit']
    temp = get_data_modbus(client, unit)
    # temp = 3
    status = 1 if temp else 2

    # insert
    temp_model = DataBase('temperature')
    temp_model.insert_one(temp=temp, status=status, sensor_id=sensor['sensor_id'])

    return {'temp': temp, 'status': status}


def read_and_save_all_device(sensors):
    return list(map(read_ans_save_one_device, sensors))


def get_data_modbus(client, unit):
    read = client.read_input_registers(address=1000, count=1, unit=unit)
    if unit == 1:
        return read.registers[0] if read.registers else None
    return float(read.registers[0])/10 if read.registers else None


def get_sensor():
    sensor_model = DataBase(table_name='sensor')
    sensor_raw_data = sensor_model.get_list()
    sensors = []
    for sensor in sensor_raw_data:
        sensors.append({
            'sensor_id': sensor[0], 'host': sensor[2], 'port': sensor[3], 'unit': sensor[4]
        })
    return sensors


def init():
    sensors = get_sensor()
    # read_and_save_all_device(sensors)


init()
