# Generated by Django 3.1.6 on 2021-02-25 00:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0090_auto_20210223_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='display_miniround',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='miniround_start',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='miniround_time',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='num_grace_minirounds',
        ),
        migrations.AddField(
            model_name='exam',
            name='submit_start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 25, 0, 20, 34, 947908, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
