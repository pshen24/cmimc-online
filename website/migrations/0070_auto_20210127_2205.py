# Generated by Django 3.1.5 on 2021-01-28 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0069_auto_20210127_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aisubmission',
            name='competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aisubmissions', to='website.competitor'),
        ),
    ]
