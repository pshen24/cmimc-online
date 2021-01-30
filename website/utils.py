from background_task import background
from django.utils.timezone import localtime, now
import math

# Lets you easily log things when in production, by calling
# log(asdf='hello world') to display {'asdf': 'hello world'}
@background(schedule=24*60*60)
def log():
    return


def miniround_sub(competitor, problem, miniround):
    time = problem.exam.miniround_end_time(miniround)
    return competitor.submissions.filter(problem=problem, submit_time__lte=time).order_by("-submit_time").first()



# score.problem.exam and score.competitor.exam should always match
# do we need to check for invalid scores?
# TODO: what if problems, tasks, or minrounds get added/removed?
def update_scores(comp):
    from website.models import Score, TaskScore, MiniRoundScore, MiniRoundTotal
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

        elif exam.is_ai:
            # create miniroundscores if they don't exist
            for i in range(exam.num_minirounds+1):
                mrs = MiniRoundScore.objects.filter(score=s, miniround=i).first()
                if mrs is None:
                    mrs = MiniRoundScore(score=s, miniround=i)
                    mrs.save()
    if exam.is_ai:
        for i in range(exam.num_minirounds):
            mrt = MiniRoundTotal.objects.filter(competitor=comp, miniround=i).first()
            if mrt is None:
                mrt = MiniRoundTotal(competitor=comp, miniround=i)
                mrt.save()




def update_competitors(team):
    from website.models import Competitor
    for exam in team.contest.exams.all():
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

# initializes all Competitors, Scores, and TaskScores
# ensures exactly one score for each (problem, competitor) pair,
# and exactly one taskscore for each (task, score) pair
def update_contest(contest):
    from website.models import MiniRoundQueue
    for team in contest.teams.all():
        update_competitors(team)
    for exam in contest.exams.all():
        if exam.is_ai:
            for i in range(exam.num_minirounds+1):
                mrq = MiniRoundQueue.objects.filter(exam=exam, miniround=i).first()
                if mrq is None:
                    mrq = MiniRoundQueue(exam=exam, miniround=i)
                    if i == 0:
                        mrq.num_games = 0
                    mrq.save()



def reset_contest(contest):
    from website.models import MiniRoundQueue
    for team in contest.teams.all():
        for c in team.competitors.all():
            c.delete()
        if contest.locked and team.mathletes.count() == 0:
            team.delete()
    for exam in contest.exams.all():
        if exam.is_ai:
            for p in exam.problems.all():
                aiprob = p.aiproblem.first()
                for g in aiprob.aigames.all():
                    g.delete()
            for i in range(exam.num_minirounds+1):
                mrq = MiniRoundQueue.objects.get(exam=exam, miniround=i)
                if i == 0:
                    mrq.num_games = 0
                else:
                    mrq.num_games = -1
                mrq.save()
            exam.display_miniround = 0
            exam.save()
        if exam.is_optimization:
            for p in exam.problems.all():
                for t in p.tasks.all():
                    t.best_raw_points = None
                    t.save()
    update_contest(contest)



def compute_weighted_avg(score, m):
    from website.models import MiniRoundScore
    grace = score.problem.exam.num_grace_minirounds
    if m < grace:
        return 0
    else:
        num = 0.0
        den = 0.0
        for i in range(m+1):
            mrs = MiniRoundScore.objects.get(score=score, miniround=i)
            w = math.sqrt(max(i-grace+1, 0))
            num += w * mrs.avg_points
            den += w
        return num / den


def update_ai_leaderboard(exam, m):
    from website.models import Score, MiniRoundScore, MiniRoundTotal

    max_dict = {}
    for p in exam.problems.all():
        max_w_avg = 0.0
        for c in exam.competitors.all():
            s = Score.objects.get(problem=p, competitor=c)
            mrs = MiniRoundScore.objects.get(score=s, miniround=m)
            mrs.weighted_avg = compute_weighted_avg(s, m)
            mrs.save()
            max_w_avg = max(max_w_avg, mrs.weighted_avg)
        max_dict[p.problem_number] = max_w_avg

    for c in exam.competitors.all():
        mrt = MiniRoundTotal.objects.get(competitor=c, miniround=m)
        mrt.total_score = 0

        for p in exam.problems.all():
            max_w_avg = max_dict[p.problem_number]
            s = Score.objects.get(problem=p, competitor=c)
            mrs = MiniRoundScore.objects.get(score=s, miniround=m)
            if max_w_avg > 0:
                mrs.norm_w_avg = mrs.weighted_avg / max_w_avg * 100
            else:
                mrs.norm_w_avg = 0
            mrs.save()
            mrt.total_score += mrs.norm_w_avg
        mrt.save()
    exam.display_miniround = m
    exam.save()


def regrade_games():
    from website.models import AIGame
    games = AIGame.objects.filter(status=3)
    for g in games:
        g.status = 0
        g.history = None
        g.save()
