# Generated by Django 3.0.7 on 2020-06-17 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shorteners', '0004_link_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='shortURL',
            new_name='_shortURL',
        ),
    ]
