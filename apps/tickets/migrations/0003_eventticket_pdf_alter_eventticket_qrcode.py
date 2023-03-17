# Generated by Django 4.1.7 on 2023-03-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_eventticket_is_expired_eventticket_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventticket',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='tickets/pdf'),
        ),
        migrations.AlterField(
            model_name='eventticket',
            name='qrcode',
            field=models.ImageField(upload_to='tickets/qrcode', verbose_name='qr code'),
        ),
    ]
