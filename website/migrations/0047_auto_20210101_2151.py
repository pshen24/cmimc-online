# Generated by Django 3.1.4 on 2021-01-02 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0046_auto_20201227_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='total_score',
            field=models.FloatField(db_index=True, default=0.0),
        ),
    ]
