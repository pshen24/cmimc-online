# Generated by Django 3.1.3 on 2020-12-11 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0032_auto_20201207_0357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='form',
            new_name='exam_type',
        ),
    ]
