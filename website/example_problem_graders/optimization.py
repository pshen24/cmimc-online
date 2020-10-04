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
}
'''

class OptGrader(BaseGrader):
    def __init__(self, problem):
        self.problem = problem
        #self.n = int(problem.grader_data["n"])
        self.n = 4

    def grade(self, submission):
        '''
        Assigns a point value to the submission, and updates the
        corresponding score and competitor's total score

        Returns: None
        '''
        raise NotImplementedError()

    def validate(self, user_input):
        '''
        Checks if the user input is a
        '''
        lines = user_input.split("\n")
        noDupes = set()
        for line in lines:
            parts = line.split()
            if len(parts) != 2:
                return False
            for part in parts: # Checks if it's actually integer
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
            x = self.n * (a - 1) + b - 1
            if x in noDupes:
                return False
            noDupes.add(x)
        return True

    # Assumes the validity of user_input
    def parse(self, user_input):
        '''
        Returns an array of 2-element arrays
        '''
        edges = []
        lines = user_input.split("\n")
        for line in lines:
            parts = line.split()
            edges.append(parts)
        return edges
    
    def calc(self, edges):
        '''
        Calculates the number of triangles in a given graph
        '''
        EdgeSet, ans = set(), 0
        for x in edges:
            EdgeSet.add(self.n * (x[0] - 1) + x[1] - 1)
        for x in edges:
            for y in edges: 
                if x[1] == y[0] and self.n * (x[0] - 1) + y[1] - 1 in EdgeSet:
                    ans += 1
        return ans
