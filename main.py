from models.machine import Machine
from models.sensor import Sensor
from models.setting import Setting
from models.parameter import Parameter


machines = Machine.get_list()
sensors = Sensor.get_list()
setting = Setting.get_list()

# print(machines)
# print(sensors)
print(setting)
