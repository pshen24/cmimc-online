from background_task import background
from django.utils import timezone
from website.models import Exam, AIGame, AISubmission, Submission, Score, MiniRoundScore, MiniRoundQueue
from background_task.models import Task
from datetime import timedelta
from website.utils import log, update_ai_leaderboard


def lastSub(competitor, problem, time):
    sub = competitor.submissions.filter(problem=problem, submit_time__lte=time).order_by("-submit_time").first()
    if sub is None:
        return ''
    else:
        return sub.text


# miniround m is graded 5*m minutes after exam starts (1 <= m <= 36)
@background
def grade_miniround(exam_id, m):
    exam = Exam.objects.get(pk=exam_id)
    comps = exam.competitors.all()
    time = exam.miniround_end_time(m)
    n = len(comps)
    games_added = 0
    for p in exam.problems.all():
        codes = [lastSub(c, p, time) for c in comps]
        ai_prob = p.aiproblem.first()
        if ai_prob.numplayers == 2:
            # 10 iterations = 20 games per player
            c = 10
            for i in range(c*(m-1), c*m):
                shift = i % (n-1) + 1
                for j1 in range(n):
                    j2 = (j1 + shift) % n
                    g = AIGame(status=-1, time=time, numplayers=2, aiproblem=ai_prob, miniround=m)
                    g.save()
                    s1 = AISubmission(game=g, seat=1, code=codes[j1], competitor=comps[j1])
                    s1.save()
                    s2 = AISubmission(game=g, seat=2, code=codes[j2], competitor=comps[j2])
                    s2.save()
                    g.status = 0    # add to queue after submissions are made
                    g.save()
                    games_added += 1
        elif ai_prob.numplayers == 3:
            # 7 iterations = 21 games per player
            c = 7
            for i in range(c*(m-1), c*m):
                x = (i + 1) % (n-2) + 1
                y = n - 1 - i % (n-1)
                if x >= y:
                    x += 1
                # guaranteed that 1 <= x,y <= n and x =/= y
                # loops over grid diagonally from top-left to bottom-right (x shifted by 1)
                # this ensures that you don't get matched with the same opponent
                # at most twice in one iteration (unless n is small or c is large)
                for j1 in range(n):
                    j2 = (j1 + x) % n
                    j3 = (j1 + y) % n
                    g = AIGame(status=-1, time=time, numplayers=3, aiproblem=ai_prob, miniround=m)
                    g.save()
                    s1 = AISubmission(game=g, seat=1, code=codes[j1], competitor=comps[j1])
                    s1.save()
                    s2 = AISubmission(game=g, seat=2, code=codes[j2], competitor=comps[j2])
                    s2.save()
                    s3 = AISubmission(game=g, seat=3, code=codes[j3], competitor=comps[j3])
                    s3.save()
                    g.status = 0    # add to queue after submissions are made
                    g.save()
                    games_added += 1
        elif ai_prob.numplayers == 0:
            g = AIGame(status=-1, time=time, numplayers=n, aiproblem=ai_prob, miniround=m)
            g.save()
            for i in range(n):
                s = AISubmission(game=g, seat=i+1, code=codes[i], competitor=comps[i])
                s.save()
            g.status = 0    # add to queue after submissions are made
            g.save()
            games_added += 1
    mrq = MiniRoundQueue.objects.get(exam=exam, miniround=m)
    mrq.num_games = games_added
    mrq.save()


@background(schedule=0)
def async_grade(submission_id):
    sub = Submission.objects.get(pk=submission_id)
    sub.grade()


@background
def check_finished_games():
    from website.models import MiniRoundQueue
    games = AIGame.objects.filter(status=2)
    for g in games:
        prob = g.aiproblem.problem
        exam = prob.exam
        m = g.miniround
        for aisub in g.aisubmissions.all():
            comp = aisub.competitor
            score = Score.objects.get(problem=prob, competitor=comp)
            mrs = MiniRoundScore.objects.filter(score=score, miniround=m).first()
            if mrs is None:
                log(error='MiniRoundScore.get returned None in check_finished_games', 
                        time=str(timezone.now()), score=str(score), miniround=m)
            else:
                if aisub.score is None:
                    log(error='aisub.score is None in check_finished_games', 
                            time=str(timezone.now()), aisub_id=str(aisub.id))
                mrs.points += aisub.score
                mrs.games += 1
                mrs.save()
        g.status=4
        g.save()
        mrq = MiniRoundQueue.objects.get(exam=exam, miniround=m)
        mrq.num_games -= 1
        mrq.save()
        if mrq.num_games == 0: # only happens once, for the last game in the miniround
            update_ai_leaderboard(exam, m)


@background
def check_graded_submissions():
    subs = AISubmission.objects.filter(status=2)
    for sub in subs:
        p = sub.problem
        t = sub.task
        c = sub.competitor
        s = Score.objects.get(problem=p, competitor=c)
        ts = TaskScore.objects.get(task=t, score=s)
        g = p.grader
        if g.better(sub.points, ts.raw_points):
            ts.raw_points = raw_points
            ts.save()

            if self.better(raw_points, task.best_raw_points):
                task.best_raw_points = raw_points
                task.save()
                for ts in task.taskscores.all():
                    ts.norm_points = self.normalize(ts.raw_points, task.best_raw_points)
                    ts.save()
                    s = ts.score
                    norms = [ts2.norm_points for ts2 in s.taskscores.all()]
                    s.points = sum(norms)/len(norms)
                    ts.score.save()
                    ts.score.competitor.update_total_score()
            else:
                taskscore.norm_points = self.normalize(raw_points, task.best_raw_points)
                taskscore.save()
                norms = [ts.norm_points for ts in score.taskscores.all()]
                score.points = sum(norms)/len(norms)
                score.save()
                score.competitor.update_total_score()





def init_all_tasks():
    Task.objects.all().delete() # Clear all previous tasks
    exams = Exam.objects.all()
    check_finished_games(schedule=0, repeat=10)
    for exam in exams:
        if exam.is_ai:
            after_end = exam.end_time + timedelta(minutes=5)
            for i in range(1, exam.num_minirounds+1):
                if timezone.now() < exam.miniround_end_time(i):
                    grade_miniround(exam.id, i, schedule=exam.miniround_end_time(i))
