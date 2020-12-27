from website.problem_graders.base import BaseGrader
from website.models import Score

class OptimizationGrader(BaseGrader):
    def __init__(self, problem):
        super().__init__(problem)
        self.num_tasks = problem.num_tasks

    def grade(self, submission, score):
        self.task = submission.task
        self.task_data = self.task.grader_data
        self.competitor = submission.competitor
        points = self.grade_task(submission.text)
        submission.points = points
        submission.is_graded = True
        submission.save()

        idx = self.task.task_number-1 # 0 indexed for list
        score = Score.objects.getScore(self.problem, self.competitor)
        if points is not None and points > score.task_scores[idx]:
            score.task_scores[idx] = points
            score.points = sum(score.task_scores)
            score.save()
            self.competitor.update_total_score()


    def grade_task(self, user_input):
        raise NotImplementedError()

