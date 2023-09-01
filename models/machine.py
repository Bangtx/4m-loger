from peewee import IntegerField, CharField
from models.base import BaseModel


class Machine(BaseModel):
    server_id = IntegerField()
    name = CharField()
    position = CharField()

    @classmethod
    def handle_select(cls, **kwargs):
        return (
            cls.select(
                cls.id, cls.server_id, cls.name
            ).dicts()
        )


