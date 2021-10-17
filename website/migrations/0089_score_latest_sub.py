# Generated by Django 3.1.6 on 2021-02-24 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0088_contest_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='latest_sub',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='score', to='website.submission'),
        ),
    ]
