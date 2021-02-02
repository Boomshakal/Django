from django.db import models


# Create your models here.
class Colors(models.Model):
    colors = models.CharField(max_length=10, unique=True)  # 蓝色

    def __str__(self):
        return self.colors


class Ball(models.Model):
    color = models.OneToOneField("Colors", on_delete=models.CASCADE)  # 与颜色表为一对一，颜色表为母表
    description = models.CharField(max_length=10)  # 描述

    def __str__(self):
        return self.description


class Clothes(models.Model):
    color = models.ForeignKey("Colors", on_delete=models.CASCADE)  # 与颜色表为外键，颜色表为母表
    description = models.CharField(max_length=10)  # 描述

    def __str__(self):
        return self.description


class Child(models.Model):
    name = models.CharField(max_length=10)  # 姓名
    favor = models.ManyToManyField('Colors')  # 与颜色表为多对多
