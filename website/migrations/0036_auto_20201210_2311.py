# Generated by Django 3.1.3 on 2020-12-11 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_auto_20201210_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='short_name',
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='name',
            field=models.CharField(help_text='The problem title that contestants see', max_length=100, unique=True),
        ),
    ]
