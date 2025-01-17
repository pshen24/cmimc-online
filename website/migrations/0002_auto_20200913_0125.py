# Generated by Django 3.1.1 on 2020-09-13 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('min_team_size', models.IntegerField()),
                ('max_team_size', models.IntegerField()),
                ('reg_start_date', models.DateTimeField(help_text='The date that registration opens, and mathletes can start forming teams')),
                ('reg_end_date', models.DateTimeField(help_text='Teams can no longer be modified after this date')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_team_exam', models.BooleanField()),
                ('show_leaderboard', models.BooleanField(help_text='Whether to allow contestants to see the leaderboard during the exam')),
                ('show_grading_score', models.BooleanField(help_text='Whether to allow contestants to see the score of a submission immediately after they submit')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='website.contest')),
            ],
        ),
        migrations.CreateModel(
            name='Mathlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mathlete', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grader_name', models.CharField(max_length=50)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='website.exam')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='website.contest')),
                ('members', models.ManyToManyField(related_name='teams', to='website.Mathlete')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='The string that the competitor submitted. Its format depends on the exam (can be an integer, source code, program output, etc)')),
                ('submit_time', models.DateTimeField()),
                ('points', models.FloatField()),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='website.competitor')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='website.problem')),
            ],
        ),
        migrations.AddField(
            model_name='competitor',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitors', to='website.exam'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='mathlete',
            field=models.ForeignKey(blank=True, help_text='If the exam is an individual exam, this is corresponding mathlete. If the exam is a team exam, this is null', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitors', to='website.mathlete'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='competitor', to='website.team'),
        ),
    ]
