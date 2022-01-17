from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name="手机号")
    status = models.BooleanField(default=True, verbose_name="状态")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user"
        verbose_name = "用户表"
        verbose_name_plural = "用户表"
