# Generated by Django 4.2.18 on 2025-02-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Скрыт'),
        ),
    ]
