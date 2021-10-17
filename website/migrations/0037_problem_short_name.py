# Generated by Django 3.1.3 on 2020-12-11 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0036_auto_20201210_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='short_name',
            field=models.CharField(default='shortname', help_text='Should be lowercase letters or numbers, no spaces', max_length=100),
            preserve_default=False,
        ),
    ]
