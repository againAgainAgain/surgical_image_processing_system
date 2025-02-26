# Generated by Django 4.2.19 on 2025-02-07 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_userinfo_age_alter_userinfo_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='token',
            field=models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='TOKEN'),
        ),
        migrations.CreateModel(
            name='SaveImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('imgpath', models.CharField(max_length=128, verbose_name='用户存储地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userinfo', verbose_name='用户')),
            ],
        ),
    ]
