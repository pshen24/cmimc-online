from background_task import background

# Lets you easily log things when in production, by calling
# log(asdf='hello world') to display {'asdf': 'hello world'}
@background(schedule=24*60*60)
def log():
    return


def reset_contest(contest):
    for team in contest.teams.all():
        teams.unregister()
        # reset task scores too

# score.problem.exam and score.competitor.exam should always match
# do we need to check for invalid scores?
# TODO: what if problems, tasks, or minrounds get added/removed?
def update_scores(comp):
    from website.models import Score, TaskScore, MiniRoundScore
    exam = comp.exam
    for problem in exam.problems.all():
        s = Score.objects.filter(problem=problem, competitor=comp).first()
        if s is None:
            s = Score(problem=problem, competitor=comp)
            s.save()

        if exam.is_optimization:
            # create taskscores if they don't exist yet
            for task in problem.tasks.all():
                ts = TaskScore.objects.filter(task=task, score=s).first()
                if ts is None:
                    ts = TaskScore(task=task, score=s)
                    ts.save()




# initializes all Competitors, Scores, and TaskScores
# ensures exactly one score for each (problem, competitor) pair,
# and exactly one taskscore for each (task, score) pair
def update_competitors(contest):
    from website.models import Competitor
    for team in contest.teams.all():
        for exam in contest.exams.all():
            # Django guarantees at most one competitor for each
            # (exam, team, mathlete) triple, so there are no duplicates

            # delete any invalid competitors
            comps = Competitor.objects.filter(exam=exam, team=team)
            for c in comps:
                if exam.is_team_exam:
                    # this shouldn't happen, unless manually set in Django Admin
                    if c.mathlete is not None:
                        c.delete()
                else:
                    # team members might have been kicked,
                    # so delete the corresponding competitor
                    if c.mathlete not in team.mathletes.all():
                        c.delete()

            # make sure all valid competitors exist, and call update_scores
            if exam.is_team_exam:
                c = Competitor.objects.filter(exam=exam, team=team, mathlete=None).first()
                if c is None:
                    c = Competitor(exam=exam, team=team, mathlete=None)
                    c.save()
                update_scores(c)
            else:
                for m in team.mathletes.all():
                    c = Competitor.objects.filter(exam=exam, team=team, mathlete=m).first()
                    if c is None:
                        c = Competitor(exam=exam, team=team, mathlete=m)
                        c.save()
                    update_scores(c)

