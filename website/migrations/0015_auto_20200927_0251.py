# Generated by Django 3.1.1 on 2020-09-27 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20200927_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='alias',
            field=models.CharField(blank=True, help_text='preferred name', max_length=100),
        ),
    ]
