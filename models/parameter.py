from models.base import BaseModel
from peewee import ForeignKeyField, FloatField, DateField, TimeField, BooleanField, fn, IntegerField
from models.machine import Machine
from datetime import date, datetime


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
        parameters = []
        for sensor in sensors:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%Y-%m-%d")

            if sensor['value'] is None:
                continue

            new_param = {
                'machine': sensor['machine'],
                'current': sensor['value'],
                'date': current_date,
                'time': current_time
            }
            parameters.append(new_param)

        if parameters:
            Parameter.insert_many(parameters).execute()