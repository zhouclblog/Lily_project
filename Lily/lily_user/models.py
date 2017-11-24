from django.db import models
from model.base_model import BaseModel
from utils.get_hash import sha_pwd
# Create your models here.


class UserInfoManager(models.Manager):

    def add_one_message(self, username, password, email):
        user_info = self.create(username=username, password=sha_pwd(password), email=email)
        return user_info



    def get_one_passport(self, username, password):
        '''根据邮箱和密码跟数据库进行比对'''
        try:
            passport = self.get(username=username, password=sha_pwd(password))
        except self.model.DoesNotExist:
            # 账户不存在
            passport = None
        return passport




class UserInfo(BaseModel):

    username = models.CharField(max_length=30, verbose_name="用户名")
    password = models.CharField(max_length=200, verbose_name="密码")
    email = models.CharField(max_length=40, verbose_name="邮箱")
    is_activate = models.BooleanField(default=False, verbose_name="激活状态")

    objects = UserInfoManager()

    class Meta(object):

        db_table = "user_info"




class AddressManager(models.Manager):
    '''地址模型管理器类'''
    def get_default_address(self, userinfo_id):
          
        '''查询指定用户的默认收货地址'''
        '''
        try:
            addr = self.get(userinfo_id=userinfo_id, is_default=True)
        except self.model.DoesNotExist:
            addr = None

        return addr
        '''
        pass


    def add_one_address(self, userinfo_id, recipient_name, recipient_addr, recipient_phone):
        '''添加收货地址'''
        # 判断用户是否有默认收货地址
        '''
        addr = self.get_default_address(userinfo_id=userinfo_id)

        if addr:
            # 存在默认地址
            is_default = False
        else:
            # 不存在默认地址
            is_default = True

        addr = self.create(userinfo_id=userinfo_id,
                           recipient_name=recipient_name,
                           recipient_addr=recipient_addr,
                           recipient_phone=recipient_phone,
                           is_default=is_default)

        return addr
        '''
        pass



class Address(BaseModel):
    '''地址模型类'''
    recipient_name = models.CharField(max_length=20, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    userinfo = models.ForeignKey('UserInfo', verbose_name='账户')

    objects = AddressManager()

    class Meta:
        db_table = 'address_info'
