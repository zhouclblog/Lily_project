from django.db import models
from model.base_model import BaseModel
from utils.get_hash import sha_pwd
# Create your models here.


class UserInfoManager(models.Manager):

    def add_one_message(self, username, password, email):
        user_info = self.create(username=username, password=sha_pwd(password), email=email)
        return user_info

    def get_one_passport(self, email, password):
        '''根据邮箱和密码跟数据库进行比对'''
        try:
            passport = self.get(email=email, password=sha_pwd(password))
        except self.model.DoesNotExist:
            # 账户不存在
            passport = None
        return passport



class UserInfo(BaseModel):

    username = models.CharField(max_length=30, verbose_name="用户名")
    password = models.CharField(max_length=30, verbose_name="密码")
    email = models.CharField(max_length=40, verbose_name="邮箱")

    is_activate = models.BooleanField(default=False, verbose_name="激活状态")

    objects = UserInfoManager()

    class Meta(object):

        db_table = "user_info"

