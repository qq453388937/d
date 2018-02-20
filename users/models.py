from django.db import models
from django.contrib.auth.models import AbstractUser  # django 自带的校验用户
from utils.models import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings


# Create your models here.


class User(AbstractUser, BaseModel):
    """用户"""

    class Meta:
        db_table = "df_users"

    def generate_active_token(self):
        """生成激活令牌token"""
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600) # 过期时间一小时
        token = serializer.dumps({"user_id": self.id})  # 返回bytes类型
        return token.decode()  # 转为字符串


class Address(BaseModel):
    """地址"""
    user = models.ForeignKey(User, verbose_name="所属用户")
    receiver_name = models.CharField(max_length=20, verbose_name="收件人")
    receiver_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    detail_addr = models.CharField(max_length=256, verbose_name="详细地址")
    zip_code = models.CharField(max_length=6, verbose_name="邮政编码")

    class Meta:
        db_table = "df_address"
