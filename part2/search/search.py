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

def solution(success_node, parents):
    if not parents[success_node][0] :
        return []
    else:
        return solution(parents[success_node][0], parents) + [parents[success_node][1]]

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
    init_node = problem.getStartState()
    frontier = util.Stack()
    explored_set = set()
    parents = {}

    frontier.push(init_node)
    parents[init_node] = (None, None) #parent state, action

    if problem.isGoalState(init_node): return solution(init_node, parents) 
    while True:
        if frontier.isEmpty(): return None
        current_node = frontier.pop()
        explored_set.add(current_node) #add (state, action, cost) to explored
        if problem.isGoalState(current_node): return solution(current_node, parents)

        available_actions = problem.getSuccessors(current_node)
        #print available_actions
        for action in available_actions:
            child_node = action[0]
            if not (child_node in explored_set):
                parents[child_node] = (current_node, action[1])
                frontier.push(child_node)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    init_node = problem.getStartState()
    frontier = util.Queue()
    explored_set = set()
    visited_set = set()
    parents = {}

    frontier.push(init_node)
    parents[init_node] = (None, None) #parent state, action

    if problem.isGoalState(init_node): return solution(init_node, parents) 
    while True:
        if frontier.isEmpty(): return None
        current_node = frontier.pop()
        explored_set.add(current_node) #add (state, action, cost) to explored
        if problem.isGoalState(current_node): return solution(current_node, parents)

        available_actions = problem.getSuccessors(current_node)
        for action in available_actions:
            child_node = action[0]
            if not (child_node in explored_set or child_node in visited_set):
                parents[child_node] = (current_node, action[1])
                visited_set.add(child_node)
                frontier.push(child_node)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    init_node = problem.getStartState()
    frontier = util.PriorityQueue()
    explored_set = set()
    parents = {}
    distance_from_start = {}

    frontier.push(init_node, 0)
    parents[init_node] = (None, None) #parent state, action
    distance_from_start[init_node] = 0

    while True:
        if frontier.isEmpty(): return None
        current_node = frontier.pop()
        explored_set.add(current_node) #add (state, action, cost) to explored
        if problem.isGoalState(current_node): return solution(current_node, parents)

        available_actions = problem.getSuccessors(current_node)
        for action in available_actions:
            child_node = action[0]
            child_action = action[1]
            child_cost = distance_from_start[current_node] + action[2]
            if not (child_node in explored_set):
                if not child_node in distance_from_start or distance_from_start[child_node] > child_cost:
                    parents[child_node] = (current_node, child_action)
                    distance_from_start[child_node] = child_cost
                    frontier.update(child_node, child_cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    init_node = problem.getStartState()
    frontier = util.PriorityQueue()
    explored_set = set()
    parents = {}
    g_distance_from_start = {}

    frontier.push(init_node, 0)
    parents[init_node] = (None, None) #parent state, action
    g_distance_from_start[init_node] = 0

    while True:
        if frontier.isEmpty(): return None
        current_node = frontier.pop()

        if problem.isGoalState(current_node): return solution(current_node, parents)
        explored_set.add(current_node) #add (state, action, cost) to explored

        available_actions = problem.getSuccessors(current_node)
        for action in available_actions:
            child_node = action[0]
            child_action = action[1]
            child_cost = g_distance_from_start[current_node] + action[2]
            if not (child_node in explored_set):
                if not child_node in g_distance_from_start or g_distance_from_start[child_node] > child_cost:
                    parents[child_node] = (current_node, child_action)
                    g_distance_from_start[child_node] = child_cost
                    cost = child_cost + heuristic(child_node, problem)
                    
                    frontier.update(child_node, cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
