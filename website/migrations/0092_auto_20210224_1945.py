# Generated by Django 3.1.6 on 2021-02-25 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0091_auto_20210224_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='submit_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
