# Generated by Django 3.1.1 on 2020-09-26 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_problem_grader_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='mathlete',
            field=models.ForeignKey(blank=True, help_text='If the exam is an individual exam, this is the             corresponding mathlete. If the exam is a team exam, this is null', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitors', to='website.mathlete'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='reg_end_date',
            field=models.DateTimeField(help_text='Teams can no longer be modified             after this date'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='reg_start_date',
            field=models.DateTimeField(help_text='The date that registration             opens, and mathletes can start forming teams'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='show_leaderboard',
            field=models.BooleanField(help_text='Whether to allow contestants             to see the leaderboard during the exam'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='show_own_scores',
            field=models.BooleanField(help_text='Whether to allow contestants             to see the score of a submission immediately after they submit'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='grader_data',
            field=models.JSONField(blank=True, help_text="Data for the             problem's grader to use. The format depends on the type of grader", null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='grader_data',
            field=models.JSONField(blank=True, help_text="Extra data that             custom graders can use. The format depends on the problem's grader", null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='text',
            field=models.TextField(help_text='The string that the competitor submitted.             Its format depends on the exam (can be an integer, source code,             program output, etc)'),
        ),
        migrations.AlterField(
            model_name='team',
            name='is_registered',
            field=models.BooleanField(default=False, help_text='The members of a             registered team are finalized and cannot be edited'),
        ),
    ]
