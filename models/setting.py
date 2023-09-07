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

    @classmethod
    def find_by_key(cls, key):
        query = cls.handle_select()
        query = query.where(cls.key == key)
        data = list(query)
        return data[0]['value']
