# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    # print   ("Start:", problem.getStartState())
    # print   ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print   ("Start's successors:", problem.getSuccessors(problem.getStartState()))
    stack = util.Stack()
    visited = set()
    start = problem.getStartState()

    stack.push((start, []))

    while not stack.isEmpty():
        # Pop the top element from the stack
        state, path = stack.pop()
        # An to state=goal , return the path
        if problem.isGoalState(state):
            return path
        # An einai unvisited, explore
        if state not in visited:
            visited.add(state)  # Mark as visited
            for successor, action, _ in problem.getSuccessors(state):
                # an o successor den einai visited, push sto stack mazi me to path
                if successor not in visited:
                    stack.push((successor, path + [action]))

    # path not found
    util.raiseNotDefined()    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue()
    visited = set()
    start = problem.getStartState()

    queue.push((start, []))

    while not queue.isEmpty():
        # dequeue to prwto stoixeio
        state, path = queue.pop()
        # An to state=goal , return the path
        if problem.isGoalState(state):
            return path
        # An einai unvisited, explore
        if state not in visited:
            visited.add(state)  # Mark as visited
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in visited:
                    queue.push((successor, path + [action]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue()
    visited = {}

    start = problem.getStartState()
    p_queue.push((start, [], 0), 0)

    while not p_queue.isEmpty():
        state, path, currentCost = p_queue.pop()

        if problem.isGoalState(state):
            return path

        if state not in visited or currentCost < visited[state]:
            visited[state] = currentCost

            for successor, action, stepCost in problem.getSuccessors(state):
                newCost = currentCost + stepCost
                priority = newCost
                h_value = heuristic(successor, problem) 
                if h_value is not None:
                    priority += heuristic(successor, problem)
                item = (successor, path + [action], newCost)
                p_queue.push(item, priority)


    util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
