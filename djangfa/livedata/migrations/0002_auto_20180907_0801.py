# Generated by Django 2.1.1 on 2018-09-07 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livedata', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='randomentry',
            old_name='question',
            new_name='random_run',
        ),
    ]