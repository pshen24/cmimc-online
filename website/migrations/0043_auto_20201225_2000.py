# Generated by Django 3.1.4 on 2020-12-26 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0042_auto_20201224_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='input_file',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]