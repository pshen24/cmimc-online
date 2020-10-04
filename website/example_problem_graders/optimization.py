from website.problem_graders.base import BaseGrader
from website.problem_graders.base import IntegerGrader

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

    def grade(self, submission):
        '''
        Assigns a point value to the submission, and updates the
        corresponding score and competitor's total score

        Returns: None
        '''
        raise NotImplementedError()

    def validate(self, user_input):
        lines = user_input.split("\n")
        for line in lines:
            parts = line.split()
            if len(parts) != 2:
                return False
            for part in parts:
                try: 
                    int(user_input)
                except ValueError:
                    return False
            if (1 > parts[0]) or (parts[0] >= parts[1]) or (parts[1] > self.n):
                return False
        return true

    def calc(self, nodes, edges):
	'''
	Calculates the number of triangles in a given graph
	'''
	EdgeSet, ans = set(), 0
	for x in edges:
	    EdgeSet.add(nodes*(x[0]-1)+x[1]-1)
	for x in edges:
	    for y in edges:
		if x[1] == y[0] and nodes*(x[0]-1)+y[1]-1 in EdgeSet:
		    ans+=1
	return ans
