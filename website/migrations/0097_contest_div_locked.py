# Generated by Django 3.1.7 on 2021-02-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0096_problem_google_form_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='div_locked',
            field=models.BooleanField(default=False),
        ),
    ]
