# Generated by Django 3.1.5 on 2021-01-15 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0051_merge_20210114_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aigame',
            name='history',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aiproblem',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aiproblems', to='website.problem'),
        ),
    ]
