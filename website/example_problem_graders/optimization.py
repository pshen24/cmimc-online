from website.problem_graders.base import BaseGrader
from website.problem_graders.integer import IntegerGrader

'''
Sample problem:
Find a graph with n vertices and m edges which minimizes the number of
triangles.
Output: m lines, each with two space-separated integers "a b", where
a and b denote an edge between vertices a and b (1 <= a < b <= n)
Scoring formula: (n choose 3) - (# of triangles)'

Expects initial grader_data to be formatted as
{
    "n": n,
    "m": m
}
'''


class OptGrader(BaseGrader):
    def __init__(self, problem):
        self.problem = problem
        # self.n = int(problem.grader_data["n"])
        self.n = problem.grader_data["n"]
        self.m = problem.grader_data["m"]

    def grade(self, submission, score):
        '''
        Assigns a point value to the submission, and updates the
        corresponding score and competitor's total score

        Returns: None
        '''
        from website.models import Score
        competitor = submission.competitor
        # score = Score.objects.getScore(self.problem, competitor)

        if not self.validate(submission.text):
            print("Invalid submission format!")
            points = 0  # TODO: notify the competitor that the submission format was invalid
        else:
            edges = self.parse(submission.text)
            points = self.n * (self.n - 1) * (self.n - 2) / 6 - self.calc(edges)

        if submission.task.task_number < len(score.task_scores):
            old = score.task_scores[submission.task.task_number]
            score.task_scores[submission.task.task_number] = max(points, old)
            score.points += score.task_scores[submission.task.task_number] - old
        else:
            while (submission.task.task_number >= len(score.task_scores)):
                score.task_scores.append(0.0)
            score.task_scores[submission.task.task_number] = points
            score.points += points

        score.save()
        competitor.update_total_score()

    def validate(self, user_input):
        '''
        Checks if the user input is a
        '''
        lines = user_input.splitlines()
        print(lines)
        noDupes = set()
        for line in lines:
            parts = line.split()
            if len(parts) != 2:
                return False
            for part in parts:  # Checks if it's actually integer
                try:
                    int(part)
                except ValueError:
                    return False
            a = int(parts[0])
            b = int(parts[1])
            if (1 > a) or (a >= b) or (b > self.n):
                return False
            # Checking for dupes
            # Note that n(a - 1) + b - 1 is a bijective mapping
            x = (a, b)
            if x in noDupes:
                return False
            noDupes.add(x)
        # Checking for size
        return len(noDupes) == self.m

    # Assumes the validity of user_input
    def parse(self, user_input):
        '''
        Returns an array of 2-element arrays
        '''
        edges = []
        lines = user_input.splitlines()
        for line in lines:
            parts = line.split()
            a = int(parts[0])
            b = int(parts[1])
            edges.append((a, b))
        return edges

    def calc(self, edges):
        '''
        Calculates the number of triangles in a given graph
        '''
        ans = 0
        for x in edges:
            for y in edges:
                if x[1] == y[0] and (x[0], y[1]) in edges:
                    ans += 1
        return ans
