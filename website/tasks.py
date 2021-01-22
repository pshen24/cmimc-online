from background_task import background
from website.models import Exam, Team
from django.utils import timezone
from website.models import AIGame, AISubmission, Submission
from background_task.models import Task

@background
def initialize_one(exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)

    #TODO make schedule, right now just puts all things at the same time

    teams = Team.objects.filter(contest=exam.contest)

    counter = 0
    curr_game = None
    for team in teams:
        if(counter==0):
            temp_game = AIGame(history=None, time=exam.start_time, numplayers=4, contest=exam)
            temp_game.save()
            curr_game = temp_game

        temp_sub = AISubmission(game=curr_game, seat = counter, code=None, team=team)
        temp_sub.save()
        counter+=1
        counter%=4

def lastSub(competitor, problem):
    sub = competitor.submissions.filter(problem=problem).order_by("-submit_time").first()
    if sub is None:
        return ''
    else:
        return sub.text

# miniround m is graded 5*m minutes after exam starts (1 <= n <= 36)
@background
def grade_miniround(exam_id, m):
    print("Grading miniround, time = " + timezone.now())
    exam = Exam.objects.get(pk=exam_id)
    comps = exam.competitors.all()
    n = len(comps)
    for p in exam.problems.all():
        codes = [lastSub(c, p) for c in comps]
        ai_prob = p.aiproblem.first()
        if ai_prob.numplayers == 2:
            # 10 iterations = 20 games per player
            c = 10
            for i in range(c*(m-1), c*m):
                shift = i % (n-1) + 1
                for j1 in range(n):
                    j2 = (j1 + shift) % n
                    g = AIGame(time=timezone.now(), numplayers=2, problem=ai_prob)
                    g.save()
                    s1 = AISubmission(game=g, seat=1, code=codes[j1], competitor=comps[j1])
                    s1.save()
                    s2 = AISubmission(game=g, seat=2, code=codes[j2], competitor=comps[j2])
                    s2.save()
        elif ai_prob.numplayers == 3:
            # 7 iterations = 21 games per player
            c = 7
            for i in range(c*(m-1), c*m):


        elif ai_prob.numplayers == 0:
        # assume 2 player game, will change later
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                game = AIGame(time=timezone.now(), numplayers=2, problem=ai_prob)
                game.save()
                s1 = AISubmission(game=game, seat=1, code=codes[i], competitor=comps[i])
                s1.save()
                s2 = AISubmission(game=game, seat=2, code=codes[j], competitor=comps[j])
                s2.save()

'''
def _main(strats):
    n = len(strats)
    scores = [0] * n 
    assert _k <= n
    out = []
    for i in range(n):
        skips = [random.randrange(1, n - 1) for _ in range(_k - 2)]
        while len(skips) != len(set(skips)):
            skips = [random.randrange(1, n - 1) for _ in range(_k - 2)]
        for j1 in range(n - 1):
            js = [j1] + [(j1 + v) % (n-1) for v in skips]
            players = [i] + [(i + j + 1) % n for j in js]
            scores_game, hist = _play(list(map(lambda x: strats[x], players)))
            _print(' '.join(map(str,players)))
            out.append(' '.join(map(lambda x:'player'+str(x), players)) + ' '
                       + str(hist))
            for u in range(_k):
                scores[players[u]] += scores_game[u]
            top_score = max(scores)
            winner_count = 0
            for u in range(_k):
                if scores_game[u] == top_score:
                    winner_count += 1
            for u in range(_k):
                if scores_game[u] == top_score:
                    scores[players[u]] += 12/winner_count
'''


@background(schedule=0)
def async_grade(submission_id):
    sub = Submission.objects.get(pk=submission_id)
    sub.grade()


def init_all_tasks():
    Task.objects.all().delete() # Clear all previous tasks
    exams = Exam.objects.all()
    for exam in exams:
        if exam.is_ai and not exam.started:
            waitTime = exam.start_time-timezone.now()
            grade_miniround(exam.id, schedule=waitTime, repeat=60*5, repeat_until=exam.end_time)
