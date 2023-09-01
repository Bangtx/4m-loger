from models.machine import Machine
from models.sensor import Sensor
from models.setting import Setting
from models.parameter import Parameter
from utils.modbus import Modbus

machines = Machine.get_list()
sensors = Sensor.get_list()
setting = Setting.get_list()

method = next(filter(lambda x: x['key'] == 'method', setting))
port = next(filter(lambda x: x['key'] == 'port', setting))
baud_rate = next(filter(lambda x: x['key'] == 'baudrate', setting))

# get data from sensor
connect_sensor = Modbus(method=method['value'], port=port['value'], baudrate=int(baud_rate['value']))
for sensor in sensors:
    sensor['value'] = connect_sensor.get_data(int(sensor['address']), 1)[0]

# insert into parameter table
Parameter.insert_sensor_values(sensors)

# upload to server
Parameter.upload_to_server()
