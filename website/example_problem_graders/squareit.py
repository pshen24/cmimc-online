from .optimization import OptimizationGrader

'''
Given an integer $n$, compute $n^2$.

Input Format:
The input consists of a positive integer $n$.

Output format:
Output the integer $n^2$.

Subtasks:
1. $1 \le n \le 10$
2. $1 \le n \le 1000$
3. $1 \le n \le 10^6$
4. $1 \le n \le 10^9$

Scoring:
You will receive 1 point for a correct answer on task 1, 2 points for task 2, 3 for task 3, and 4 for task 4, for a total of 10 points.

Sample Input:
4

Sample Output:
16


Task data for task 3, n=4:
{
    "answer": 16,
    "weight": 3
}
'''

class SquareIt(OptimizationGrader):
    # Returns the number of points that the submission should receive
    # If the input is invalid, return None (this is temporary,
    # later it will return a more detailed error message)
    #
    # self.num_tasks = number of tasks in problem
    # self.task_number = 1-indexed task number
    # self.task_data = custom task grader_data that you can set (JSON object)
    def grade_task(self, user_input):
        answer = self.task_data["answer"]
        weight = self.task_data["weight"]
        try:
            i = int(user_input)
            if i == answer:
                return weight # tasks are weighted, with harder tasks giving more points
            else:
                return 0
        except ValueError:
            return None

