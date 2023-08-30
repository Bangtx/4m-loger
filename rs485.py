import time
# from noisuytt import noisuy
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Defaults

Defaults.RetryOnEmpty = True
Defaults.Timeout = 5
Defaults.Retries = 5


def Get_Data_Modbus():
    client = ModbusClient(method='rtu', port='COM2', timeout=2, stopbits=1, bytesize=8, parity='N', baudrate=19200)
    client.connect()
    Device1 = client.read_input_registers(address=1000, count=1, unit=1)
    Device2 = client.read_input_registers(address=1000, count=1, unit=2)
    Device3 = client.read_input_registers(address=1000, count=1, unit=3)
    Device4 = client.read_input_registers(address=1000, count=1, unit=4)
    # Device2 = client.read_input_registers(address=16, count=2, unit=2)
    Temp1_In_Modbus = Device1.registers[0]
    Temp2_In_Modbus = Device2.registers[0]
    Temp3_In_Modbus = Device3.registers[0]
    Temp4_In_Modbus = Device4.registers[0]
    print(Device1.__dict__)
    # print(Device2.__dict__)
    time.sleep(1)
    print(float(Temp1_In_Modbus))
    print(float(Temp2_In_Modbus))
    print(float(Temp3_In_Modbus))
    print(float(Temp4_In_Modbus))



Get_Data_Modbus()