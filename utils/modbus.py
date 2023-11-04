import time
# from noisuytt import noisuy
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Defaults
from pymodbus.exceptions import ModbusIOException, ModbusException

Defaults.RetryOnEmpty = True
Defaults.Timeout = 5
Defaults.Retries = 5


class Modbus:
    def __init__(self, method='rtu', port='COM4', baudrate=57600):
        self.client = ModbusClient(
            method=method, port=port, timeout=2, stopbits=1, bytesize=8, parity='N', baudrate=baudrate
        )

    def get_data(self, address, count, unit=1):
        self.client.connect()
        try:
            device = self.client.read_holding_registers(address=address, count=count, unit=unit)
            # print(address, device)
            return device.registers
        except (ModbusIOException, ModbusException) as e:
            return [None] * count
        except:
            return [None] * count
        finally:
            self.client.close()

