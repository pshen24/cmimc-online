'''Sample problem:
Find a graph with n vertices and m edges which minimizes the number of
triangles.
Output: m lines, each with two space-separated integers "a b", where
a and b denote an edge between vertices a and b (1 <= a, b <= n, a != b)
Scoring formula: (n choose 3) - (# of triangles)'
'''

class BaseGrader:
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
        '''
        Checks whether the user's input is in an acceptable format

        Returns: bool
        '''
        raise NotImplementedError()

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
