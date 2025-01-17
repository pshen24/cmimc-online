# Generated by Django 3.1.1 on 2020-09-13 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20200913_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitor', to='website.team'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
