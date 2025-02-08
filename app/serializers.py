from rest_framework import serializers,exceptions
from app import models


class UserModelSerializer(serializers.ModelSerializer):
    # confirm_password=serializers.CharField(write_only=True)
    captcha=serializers.CharField(write_only=True)
    captcha_key=serializers.CharField(write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "password", 'captcha', 'captcha_key', "token"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only":True},
            "captcha": {"read_only":True},
            "captcha_key": {"read_only":True}
        }

    # def validate_confirm_password(self, value):
    #     # value=confirm_password
    #     # self.inital_data：fields的全部字段值
    #     password = self.initial_data.get("password")
    #     if password != value:
    #         raise exceptions.ValidationError("密码不一致！")
    #     return value


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "password"]


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SaveImages
        fields = ['id', 'image', 'imgpath', 'user']