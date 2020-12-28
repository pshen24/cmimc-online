# Generated by Django 3.1.3 on 2020-12-11 03:21

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0034_auto_20201210_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='input_link',
        ),
        migrations.AddField(
            model_name='contest',
            name='short_name',
            field=models.CharField(default='temp', help_text='should be lowercase letters or numbers, no spaces', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='input_file',
            field=models.FileField(default='file.txt', upload_to=website.models.input_data_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]