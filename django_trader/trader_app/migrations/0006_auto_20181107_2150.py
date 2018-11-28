# Generated by Django 2.0.2 on 2018-11-07 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trader_app', '0005_candlestick'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_site', models.URLField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trader_app.User')),
            ],
        ),
        migrations.DeleteModel(
            name='CandleStick',
        ),
    ]