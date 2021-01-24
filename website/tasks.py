from background_task import background
from django.utils import timezone
from website.models import Exam, AIGame, AISubmission, Submission, Score, MiniRoundScore
from background_task.models import Task
from datetime import timedelta




def lastSub(competitor, problem):
    sub = competitor.submissions.filter(problem=problem).order_by("-submit_time").first()
    if sub is None:
        return ''
    else:
        return sub.text

# miniround m is graded 5*m minutes after exam starts (1 <= n <= 36)
@background
def grade_miniround(exam_id, m):
    # print("Grading miniround, time = ", timezone.now())
    exam = Exam.objects.get(pk=exam_id)
    comps = exam.competitors.all()
    time = exam.start_time + m*exam.miniround_time
    n = len(comps)
    for p in exam.problems.all():
        # create MiniRoundScores
        for c in comps:
            score = Score.objects.get(problem=p, competitor=c)
            mrs = MiniRoundScore.objects.filter(score=score, miniround=m).first()
            if mrs is None:
                mrs = MiniRoundScore(score=score, miniround=m)
            mrs.points = 0
            mrs.save()
        codes = [lastSub(c, p) for c in comps]
        ai_prob = p.aiproblem.first()
        if ai_prob.numplayers == 2:
            # 10 iterations = 20 games per player
            c = 10
            for i in range(c*(m-1), c*m):
                shift = i % (n-1) + 1
                for j1 in range(n):
                    j2 = (j1 + shift) % n
                    # print(j1, j2)
                    g = AIGame(time=time, numplayers=2, aiproblem=ai_prob, miniround=m)
                    g.save()
                    s1 = AISubmission(game=g, seat=1, code=codes[j1], competitor=comps[j1])
                    s1.save()
                    s2 = AISubmission(game=g, seat=2, code=codes[j2], competitor=comps[j2])
                    s2.save()
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
                    # print(j1, j2, j3)
                    g = AIGame(time=time, numplayers=3, aiproblem=ai_prob, miniround=m)
                    g.save()
                    s1 = AISubmission(game=g, seat=1, code=codes[j1], competitor=comps[j1])
                    s1.save()
                    s2 = AISubmission(game=g, seat=2, code=codes[j2], competitor=comps[j2])
                    s2.save()
                    s3 = AISubmission(game=g, seat=3, code=codes[j3], competitor=comps[j3])
                    s3.save()
        elif ai_prob.numplayers == 0:
            g = AIGame(time=time, numplayers=n, aiproblem=ai_prob, miniround=m)
            g.save()
            for i in range(n):
                s = AISubmission(game=g, seat=i+1, code=codes[i], competitor=comps[i])
                s.save()


@background(schedule=0)
def async_grade(submission_id):
    sub = Submission.objects.get(pk=submission_id)
    sub.grade()


@background
def check_finished_games(exam_id):
    exam = Exam.objects.get(pk=exam_id)
    games = AIGame.objects.filter(status=2, aiproblem__problem__exam=exam)
    for g in games:
        m = g.miniround
        for aisub in g.aisubmissions.all():
            comp = aisub.competitor
            prob = aisub.game.aiproblem.problem
            score = Score.objects.get(problem=prob, competitor=comp)
            mrs = MiniRoundScore.objects.filter(score=score, miniround=m).first()
            if mrs is None:
                mrs = MiniRoundScore(score=score, miniround=m)
            mrs.points += aisub.score
            mrs.save()
        g.status=4
        g.save()

    # update leaderboard
    for p in exam.problems.all():
        for c in exam.competitors.all():
            s = Score.objects.get(problem=p, competitor=c)
            s.points = sum([mrs.points for mrs in s.miniroundscores.all()])
            s.save()


def init_all_tasks():
    print('init tasks')
    Task.objects.all().delete() # Clear all previous tasks
    exams = Exam.objects.all()
    for exam in exams:
        if exam.is_ai:
            check_finished_games(exam.id, repeat=10, repeat_until=exam.end_time + timedelta(minutes=1))
            exam_time = exam.end_time - exam.start_time
            num_minirounds = exam_time // exam.miniround_time 
            for i in range(1, num_minirounds+1):
                if timezone.now() < exam.start_time + i*exam.miniround_time:
                    grade_miniround(exam.id, i, schedule=exam.start_time + i*exam.miniround_time)
