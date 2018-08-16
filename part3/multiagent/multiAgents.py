# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        min_ghost = min(newGhostStates, key=lambda x: manhattanDistance(x.getPosition(), newPos)) if newGhostStates else None
        min_food = min(newFood.asList(), key=lambda x: manhattanDistance(x, newPos)) if newFood.asList() else None

        ghost_dist = manhattanDistance(min_ghost.getPosition(), newPos) if min_ghost else 1000
        food_dist = manhattanDistance(min_food, newPos) if min_food else 0
        food_no = len(newFood.asList())

        value = 1000000 - 100*food_no - food_dist
        if ghost_dist <= 5:
          value = value * ghost_dist/5.0

        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def minmax_pacman(self, gameState, current_depth):
        pacman_available_actions = gameState.getLegalActions(0)
        if current_depth == self.depth or not pacman_available_actions :
          return self.evaluationFunction(gameState)

        best_pacman_option_value = -999999999
        best_pacman_option = pacman_available_actions[0]

        for pacman_action in pacman_available_actions :
          new_gameState = gameState.generateSuccessor(0, pacman_action)
          new_state_evaluation = self.minmax_ghosts(new_gameState, 1, current_depth)
          #best_pacman_option_value = max(new_state_evaluation, best_pacman_option_value)
          if new_state_evaluation > best_pacman_option_value :
            best_pacman_option_value = new_state_evaluation
            best_pacman_option = pacman_action
          
        #print best_pacman_option if current_depth==self.depth else best_pacman_option_value
        return best_pacman_option if current_depth==0 else best_pacman_option_value

    def minmax_ghosts(self, gameState, ghost_no, current_depth):
        ghost_available_actions = gameState.getLegalActions(ghost_no)
        if current_depth == self.depth or not ghost_available_actions:
          return self.evaluationFunction(gameState)

        best_ghost_option_value = 9999999999
        best_ghost_option = ghost_available_actions[0]

        for ghost_action in ghost_available_actions :
          new_gameState = gameState.generateSuccessor(ghost_no, ghost_action)
          if ghost_no < gameState.getNumAgents()-1:
            #run for the next ghost
            new_state_evaluation = self.minmax_ghosts(new_gameState, ghost_no+1, current_depth)
          else:
            #run for pacman
            new_state_evaluation = self.minmax_pacman(new_gameState, current_depth+1)

          best_ghost_option_value= min(new_state_evaluation, best_ghost_option_value)
        #print best_ghost_option_value
        return best_ghost_option_value

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        best_action = self.minmax_pacman(gameState, 0)
        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minmax_pacman(self, gameState, current_depth, a, b):
        pacman_available_actions = gameState.getLegalActions(0)
        if current_depth == self.depth or not pacman_available_actions :
          return self.evaluationFunction(gameState)

        best_pacman_option_value = -999999999
        best_pacman_option = pacman_available_actions[0]

        for pacman_action in pacman_available_actions :
          new_gameState = gameState.generateSuccessor(0, pacman_action)
          new_state_evaluation = self.minmax_ghosts(new_gameState, 1, current_depth, a, b)

          if new_state_evaluation > best_pacman_option_value :
            best_pacman_option_value = new_state_evaluation
            best_pacman_option = pacman_action

          if new_state_evaluation > b :
            break
          a = max(a, new_state_evaluation)
          
        #print best_pacman_option if current_depth==self.depth else best_pacman_option_value
        return best_pacman_option if current_depth==0 else best_pacman_option_value

    def minmax_ghosts(self, gameState, ghost_no, current_depth, a, b):
        ghost_available_actions = gameState.getLegalActions(ghost_no)
        if current_depth == self.depth or not ghost_available_actions:
          return self.evaluationFunction(gameState)

        best_ghost_option_value = 9999999999
        best_ghost_option = ghost_available_actions[0]

        for ghost_action in ghost_available_actions :
          new_gameState = gameState.generateSuccessor(ghost_no, ghost_action)
          if ghost_no < gameState.getNumAgents()-1:
            #run for the next ghost
            new_state_evaluation = self.minmax_ghosts(new_gameState, ghost_no+1, current_depth, a, b)
          else:
            #run for pacman
            new_state_evaluation = self.minmax_pacman(new_gameState, current_depth+1, a, b)
          best_ghost_option_value= min(new_state_evaluation, best_ghost_option_value)

          if new_state_evaluation < a :
            break
          b = min(b, new_state_evaluation)
        #print best_ghost_option_value
        return best_ghost_option_value

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        best_action = self.minmax_pacman(gameState, 0, -9999999, 9999999)
        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax_pacman(self, gameState, current_depth):
        pacman_available_actions = gameState.getLegalActions(0)
        if current_depth == self.depth or not pacman_available_actions :
          return self.evaluationFunction(gameState)

        best_pacman_option_value = -999999999
        best_pacman_option = pacman_available_actions[0]

        for pacman_action in pacman_available_actions :
          new_gameState = gameState.generateSuccessor(0, pacman_action)
          new_state_evaluation = self.expectimax_ghosts(new_gameState, 1, current_depth)

          if new_state_evaluation > best_pacman_option_value :
            best_pacman_option_value = new_state_evaluation
            best_pacman_option = pacman_action

        #print best_pacman_option if current_depth==2 else best_pacman_option_value
        return best_pacman_option if current_depth==0 else best_pacman_option_value

    def expectimax_ghosts(self, gameState, ghost_no, current_depth):
        ghost_available_actions = gameState.getLegalActions(ghost_no)
        if current_depth == self.depth or not ghost_available_actions:
          return self.evaluationFunction(gameState)

        expected_ghost_option_value = 0.0

        for ghost_action in ghost_available_actions :
          new_gameState = gameState.generateSuccessor(ghost_no, ghost_action)
          if ghost_no < gameState.getNumAgents()-1:
            #run for the next ghost
            new_state_evaluation = self.expectimax_ghosts(new_gameState, ghost_no+1, current_depth)
          else:
            #run for pacman
            new_state_evaluation = self.expectimax_pacman(new_gameState, current_depth+1)

          expected_ghost_option_value += new_state_evaluation

        return expected_ghost_option_value/float(len(ghost_available_actions))

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        best_action = self.expectimax_pacman(gameState, 0)
        return best_action


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    lost = currentGameState.isLose()
    won = lost = currentGameState.isWin()
    capsules = currentGameState.getCapsules()

    if won :
      return 10000
    elif lost :
      return 0.0
    
    min_ghost = min(ghosts, key=lambda x: manhattanDistance(x.getPosition(), position)) if ghosts else None
    min_food = min(food, key=lambda x: manhattanDistance(x, position)) if food else None

    ghost_dist = manhattanDistance(min_ghost.getPosition(), position) if min_ghost else 1000
    food_dist = manhattanDistance(min_food, position) if min_food else 0


    value = score - 10*len(capsules) - 10*len(food) - 2*food_dist
    if ghost_dist <= 3 :
      value -= 40*ghost_dist

    return value


    

# Abbreviation
better = betterEvaluationFunction

