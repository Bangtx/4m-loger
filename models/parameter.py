import requests
from models.base import BaseModel
from peewee import ForeignKeyField, FloatField, DateField, TimeField, BooleanField, fn, IntegerField
from models.machine import Machine
from datetime import date, datetime
from models.setting import Setting
from utils.common import login, to_current
from json import dumps


class Parameter(BaseModel):
    company_id = IntegerField()
    machine = ForeignKeyField(Machine)
    temperature_1 = FloatField()
    temperature_2 = FloatField()
    temperature_3 = FloatField()
    temperature_4 = FloatField()
    current = FloatField()
    date = DateField()
    time = TimeField()
    is_running = BooleanField()
    is_problem = BooleanField()
    is_uploaded = BooleanField()

    @classmethod
    def handle_select(cls, **kwargs):
        query = (
            cls.select(
                cls.id,
                cls.company_id,
                cls.machine,
                cls.temperature_1,
                cls.temperature_2,
                cls.temperature_3,
                cls.temperature_4,
                cls.current,
                cls.date,
                cls.time,
                cls.is_running,
                cls.is_problem,
                cls.is_uploaded
            ).join(
                Machine, on=Machine.id == cls.machine
            ).dicts()
        )

        return query

    @classmethod
    def get_latest_param(cls, machine):
        query = cls.handle_select()
        query = query.where(cls.active, cls.machine == machine)
        query = query.order_by(cls.id.desc()).limit(1)
        param = list(query)
        return param[0] if param else None

    @classmethod
    def insert_sensor_values(cls, sensors):
        setting = Setting.get_list()
        company = next(filter(lambda x: x['key'] == 'company', setting))

        parameters = []
        for sensor in sensors:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%Y-%m-%d")

            if sensor['value'] is None:
                continue

            new_param = {
                'company_id': company['value'],
                'machine': sensor['machine'],
                'current': to_current(sensor['value']),
                'date': current_date,
                'time': current_time
            }
            parameters.append(new_param)

        if parameters:
            Parameter.insert_many(parameters).execute()

    @classmethod
    def upload_to_server(cls):
        # get all data have not been uploaded yet
        old_params = Parameter.get_list(is_uploaded=False)
        body = cls.__to_body(old_params)

        token = login()

        if token:
            api_url = Setting.find_by_key('api_url')
            # api_url = 'http://172.17.0.1:1001'

            response = requests.post(
                f'{api_url}/parameter',
                data=dumps(body),
                headers={"Authorization": f"Bearer {token}"}
            )
            # print(response.json())
            cls.update(is_uploaded=True).where(cls.is_uploaded == False).execute()

    @classmethod
    def __to_body(cls, params):
        result = []

        machines = Machine.get_list()

        for param in params:
            machine = list(filter(lambda x: x['id'] == param['machine'], machines))
            machine = machine[0]
            result.append({
                'company': param['company_id'],
                'machine': machine['server_id'],
                'current': param['current'],
                'date': str(param['date']),
                'time': str(param['time']),
                'is_running': param['is_running'],
                'is_problem': param['is_problem']
            })
        return result
