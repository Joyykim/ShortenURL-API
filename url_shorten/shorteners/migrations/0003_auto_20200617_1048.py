# Generated by Django 3.0.7 on 2020-06-17 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorteners', '0002_auto_20200616_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='shortURL',
            field=models.CharField(max_length=200),
        ),
    ]
