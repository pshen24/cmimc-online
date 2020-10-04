from website.problem_graders.base import IntegerGrader

'''
Sample problem:
Find a graph with n vertices and m edges which minimizes the number of
triangles.
Output: m lines, each with two space-separated integers "a b", where
a and b denote an edge between vertices a and b (1 <= a, b <= n, a != b)
Scoring formula: (n choose 3) - (# of triangles)'
'''

class OptGrader:
    def __init__(self, problem):
        self.problem = problem

    def grade(self, submission):
        '''
        Assigns a point value to the submission, and updates the
        corresponding score and competitor's total score

        Returns: None
        '''
        raise NotImplementedError()

    def validate(self, user_input):
        lines = split(user_input, "\n")
        for line in lines:
            parts = split(line)
            if len(parts) != 2:
                return false
            for part in parts:
                if !validate(part):
                    return false
        return true
