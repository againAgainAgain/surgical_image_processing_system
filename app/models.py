from django.db import models

# 执行以下2个命令可以自动在数据库中创建app_userinfo表（id自增）
## python manage.py makemigrations
## python manage.py migrate
class UserInfo(models.Model):
    username=models.CharField(verbose_name="用户名",max_length=32)
    password=models.CharField(verbose_name="密码",max_length=64)
    age=models.IntegerField(verbose_name="年龄", null=True, blank=True, db_index=True)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True, db_index=True)

class SaveImages(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    imgpath = models.CharField(verbose_name="用户存储地址", max_length=128)
    user=models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
