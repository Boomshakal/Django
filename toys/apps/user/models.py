import mongoengine
from django.db import models
from bson import ObjectId


# Create your models here.


class User(mongoengine.Document):
    _id = ObjectId()
    account = mongoengine.StringField(max_length=100)
    password = mongoengine.StringField(max_length=100)
    email = mongoengine.EmailField()

    def __repr__(self):
        return self.account

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
