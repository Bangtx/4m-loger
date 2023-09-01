from peewee import CharField, ForeignKeyField, fn
from models.base import BaseModel
from models.machine import Machine
from utils.common import json_build_object


class Sensor(BaseModel):
    name = CharField()
    address = CharField()
    machine = ForeignKeyField(Machine)
    position = CharField()

    @classmethod
    def handle_select(cls, **kwargs):
        return (
            cls.select(
                cls.id,
                cls.address,
                cls.machine,
                cls.position
            ).join(
                Machine, on=Machine.id == cls.machine
            ).where(
                cls.active, Machine.active
            ).dicts()
        )