from peewee import IntegerField, CharField, ForeignKeyField
from models.base import BaseModel


class Setting(BaseModel):
    key = CharField()
    value = CharField()

    @classmethod
    def handle_select(cls, **kwargs):
        return (
            cls.select(
                cls.id, cls.key, cls.value
            ).dicts()
        )