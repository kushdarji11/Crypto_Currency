# Generated by Django 3.1.6 on 2022-04-03 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='total_price_int',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
