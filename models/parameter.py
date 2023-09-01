from models.base import BaseModel
from peewee import ForeignKeyField, FloatField, DateField, TimeField, BooleanField, fn, IntegerField
from models.machine import Machine


class Parameter(BaseModel):
    company = IntegerField()
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

    @classmethod
    def handle_select(cls, **kwargs):
        query = (
            cls.select(
                cls.id,
                cls.company,
                cls.machine,
                cls.temperature_1,
                cls.temperature_2,
                cls.temperature_3,
                cls.temperature_4,
                cls.current,
                cls.date,
                cls.time,
                cls.is_running,
                cls.is_problem
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
