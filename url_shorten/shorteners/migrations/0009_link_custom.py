# Generated by Django 3.0.7 on 2020-06-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorteners', '0008_auto_20200618_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='custom',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
