# Generated by Django 4.0.3 on 2022-08-27 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_food_admin_hoteladmin_admin_room_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hoteladmin',
            name='password2',
        ),
    ]
