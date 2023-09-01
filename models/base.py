from peewee import Model, BooleanField, BigIntegerField
from playhouse.postgres_ext import DateTimeTZField
from config.database import db
from datetime import datetime, timezone
from peewee import DoesNotExist
from operator import attrgetter
import base64
from playhouse.shortcuts import model_to_dict
from config.database import db


class BaseModel(Model):
    created_at = DateTimeTZField(default=datetime.now)
    created_by = BigIntegerField()
    modified_at = DateTimeTZField()
    modified_by = BigIntegerField()
    deleted_at = DateTimeTZField()
    deleted_by = BigIntegerField()
    active = BooleanField(default=True)

    class Meta:
        database = db

    @classmethod
    def get_one(cls, id: int, **kwargs):
        to_dict = kwargs['to_dict'] if 'to_dict' in kwargs else True
        try:
            data = cls.get_by_id(id)
            if to_dict:
                return model_to_dict(data)
            return data
        except DoesNotExist:
            print(f"{cls.__name__} not found")

    @classmethod
    def handle_select(cls, **kwargs):
        to_dict = kwargs['to_dict'] if 'to_dict' in kwargs else True
        if to_dict:
            return cls.select().dicts()
        return cls.select()

    @classmethod
    def get_list(cls, **kwargs):
        query = cls.handle_select(**kwargs)

        query = query.where(cls.active)
        for key, value in kwargs.items():
            if key in cls._meta.fields:
                if value is not None:
                    query = query.where(attrgetter(key)(cls) == value)
            if key == 'ids':
                query = query.where(cls.id << value)

        query = query.order_by(cls.id)

        return list(query)

    @classmethod
    def update_one(cls, id: int, data_update: dict, **kwargs):
        try:
            query = cls.update(**data_update, modified_at=datetime.now(timezone.utc)).where(
                cls.id == id
            )
            query.execute()

            data = cls.get_one(id, **kwargs)
            return data
        except DoesNotExist:
            print(f"{cls.__name__} not found")

    @classmethod
    def soft_delete(cls, id: int, deleted_by: int = None):
        try:
            data = cls.get_by_id(id)
            data.active = False
            data.deleted_at = datetime.now(timezone.utc)
            data.deleted_by = deleted_by
            data.save()
            return {"detail": f"Deleted {cls.__name__} {id}"}
        except DoesNotExist:
            print(f"{cls.__name__} not found")

    @classmethod
    def soft_delete_many(cls, ids, deleted_by: int = None):
        try:
            if (ids is None) or (len(ids) == 0):
                return "Nothing to delete"

            query = (cls.update(
                {
                    'active': False,
                    'deleted_at': datetime.now(timezone.utc),
                    'deleted_by': deleted_by
                }
            ).where(
                cls.id.in_(ids)
            ))

            query.execute()
            return {"detail": f"Deleted {cls.__name__} {','.join(str(x) for x in ids)}"}
        except DoesNotExist:
            print(f"{cls.__name__} not found")
            

