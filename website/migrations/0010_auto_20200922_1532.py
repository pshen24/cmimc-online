# Generated by Django 3.1.1 on 2020-09-22 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20200913_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='show_submission_scores',
            new_name='show_own_scores',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='points',
        ),
        migrations.AddField(
            model_name='competitor',
            name='total_score',
            field=models.IntegerField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='competitor',
            unique_together={('exam', 'team', 'mathlete')},
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField(default=0.0)),
                ('grader_data', models.JSONField(blank=True, help_text="Extra data that custom graders can use. The format depends on the problem's grader", null=True)),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='website.competitor')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='website.problem')),
            ],
            options={
                'unique_together': {('problem', 'competitor')},
            },
        ),
    ]
