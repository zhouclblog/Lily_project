from django.db import models
from model.base_model import BaseModel
from utils.get_hash import sha_pwd
# Create your models here.


class UserInfoManager(models.Manager):

    def add_one_message(self, username, password, email):
        user_info = self.create(username=username, password=sha_pwd(password), email=email)
        return user_info

class UserInfo(BaseModel):

    username = models.CharField(max_length=30, verbose_name="用户名")
    password = models.CharField(max_length=30, verbose_name="密码")
    email = models.CharField(max_length=40, verbose_name="邮箱")

    is_activate = models.BooleanField(default=False, verbose_name="激活状态")

    objects = UserInfoManager()

    class Meta(object):

        db_table = "user_info"
