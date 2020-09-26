from website.problem_graders.base import BaseGrader

'''
IntegerGrader is used for most math exams. 
It grades problems which have integer answers.
Negative integers are allowed.

Expects initial grader_data to be formatted as
{
    "answer": "ANSWER",
    "keep_best": "KEEP_BEST"
}
where ANSWER is the integer answer to the problem,
and KEEP_BEST is a boolean that indicates whether to keep the best
submission's score, instead of overriding it with the most recent submission.
'''

class IntegerGrader(BaseGrader):
    def __init__(self, problem):
        super().__init__(problem)
        self.answer = int(problem.grader_data["answer"])
        self.keep_best = bool(problem.grader_data["keep_best"])

    def grade(self, submission):
        from website.models import Score
        competitor = submission.competitor
        score = Score.objects.getScore(self.problem, competitor)

        # the submission should've been validated before they submit,
        # but this is just a precaution
        if not self.validate(submission.text):
            points = 0 # TODO: notify the competitor that the submission format was invalid
        elif int(submission.text) == self.answer:
            points = 1
        else:
            points = 0

        if self.keep_best:
            score.points = max(score.points, points)
        else:
            score.points = points
        score.save()

        competitor.update_total_score()



    # there are many kinds of negative signs:
    # https://en.wikipedia.org/wiki/Wikipedia:Hyphens_and_dashes
    # should we count all of these as valid?
    # Python only counts the hyphen as valid
    def validate(self, user_input):
        try: 
            int(user_input)
            return True
        except ValueError:
            return False

