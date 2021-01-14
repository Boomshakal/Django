import mongoengine
from django.db import models
from bson import ObjectId
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    '''
    用户
    '''
    name = mongoengine.StringField(verbose_name='姓名', max_length=30, null=True ,blank=True, help_text="姓名")
    birthday = mongoengine.DateField(verbose_name='出生年月', null=True, blank=True, help_text="出生日期")
    gender = mongoengine.StringField(verbose_name='性别', max_length=6, choices=(('male',u'男'),('female','女')), default="male", help_text="性别(male/female)")
    mobile = mongoengine.StringField(verbose_name='电话', null=True, blank=True, max_length=11, help_text="手机号")
    email = mongoengine.StringField(verbose_name='邮箱', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Address(mongoengine.Document):
    _id = ObjectId()
    user = ObjectId()
    address = mongoengine.StringField(max_length=500)
    detal_choices = ((0, '台州'), (1, '深圳'), (2, '长沙'))
    detal = mongoengine.IntField(choices=detal_choices, default=1)
    is_default = mongoengine.BooleanField()
