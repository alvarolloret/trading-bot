# Generated by Django 2.0.2 on 2018-11-07 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader_app', '0003_auto_20181107_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='candlestick_4h_eth_usdt',
            name='average',
            field=models.FloatField(default=0),
        ),
    ]