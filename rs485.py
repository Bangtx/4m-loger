import time
# from noisuytt import noisuy
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Defaults
from pymodbus.exceptions import ModbusIOException, ModbusException

Defaults.RetryOnEmpty = True
Defaults.Timeout = 5
Defaults.Retries = 5


def get_data_modbus():
    client = ModbusClient(method='rtu', port='COM4', timeout=2, stopbits=1, bytesize=8, parity='N', baudrate=57600)
    client.connect()
    while True:
        try:
            device_1 = client.read_holding_registers(address=16, count=4, unit=1)
            device_2 = client.read_holding_registers(address=17, count=1, unit=1)
            device_3 = client.read_holding_registers(address=18, count=1, unit=1)
            device_4 = client.read_holding_registers(address=19, count=1, unit=1)
            # print(device_1.registers, device_2.registers, device_3.registers, device_4.registers)
            print(device_1.registers)
            time.sleep(1)
        except (ModbusIOException, ModbusException) as e:
            print("Modbus communication error:", e)
        finally:
            client.close()
    device_1 = client.read_holding_registers(address=17, count=5, unit=1)




get_data_modbus()