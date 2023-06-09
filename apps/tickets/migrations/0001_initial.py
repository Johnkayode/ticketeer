# Generated by Django 4.1.7 on 2023-03-15 16:37

import apps.tickets.utils
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTicket',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted')),
                ('is_deleted', models.BooleanField(default=False)),
                ('reference', models.CharField(default=apps.tickets.utils.generate_ticket_reference, max_length=100, unique=True)),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('qrcode', models.ImageField(upload_to='', verbose_name='qr code')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
