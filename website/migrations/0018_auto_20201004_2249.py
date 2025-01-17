# Generated by Django 3.1.1 on 2020-10-05 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_auto_20201003_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='show_own_scores',
            field=models.BooleanField(help_text='Whether to allow contestants             to see their scores during the exam'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submit_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
