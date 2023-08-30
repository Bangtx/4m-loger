

def get_data_modbus(client, unit):
    read = client.read_input_registers(address=1000, count=1, unit=2)
    print(read.registers, 'unit', unit)
    return read.registers[0] if read.registers else None
