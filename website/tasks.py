from background_task import background
from website.models import Exam, Team
from django.utils import timezone
from website.models import AIGame, AISubmission

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

@background
def grade_miniround(exam_id):
    print("Grading miniround, time = " + timezone.now())
    exam = Exam.objects.get(pk=exam_id)
    comps = exam.competitors.all()
    n = len(comps)
    for p in exam.problems.all():
        codes = [lastSub(c, p) for c in comps]
        ai_prob = p.aiproblem.first()
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




def init_all_tasks():
    exams = Exam.objects.all()
    for exam in exams:
        if exam.is_ai and not exam.started:
            waitTime = exam.start_time-timezone.now()
            grade_miniround(exam.id, schedule=waitTime, repeat=60*5, repeat_until=exam.end_time)
