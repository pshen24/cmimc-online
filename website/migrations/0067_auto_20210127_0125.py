# Generated by Django 3.1.5 on 2021-01-27 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0066_auto_20210126_2241'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='miniroundscore',
            unique_together={('score', 'miniround')},
        ),
    ]
