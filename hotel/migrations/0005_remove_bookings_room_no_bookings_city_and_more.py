# Generated by Django 4.1 on 2022-08-31 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_roomtypes_alter_room_room_type'),
        ('hotel', '0004_payments_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='room_no',
        ),
        migrations.AddField(
            model_name='bookings',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='portal.hoteladmin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookings',
            name='room_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='portal.roomtypes'),
            preserve_default=False,
        ),
    ]
