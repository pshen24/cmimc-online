# Generated by Django 3.1.5 on 2021-01-31 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0073_exam_num_grace_minirounds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='task',
        ),
        migrations.AddField(
            model_name='problem',
            name='grader_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
